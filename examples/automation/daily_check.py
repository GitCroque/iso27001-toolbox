#!/usr/bin/env python3
"""
Daily ISO 27001 Health Check Script

This script performs automated daily checks on your ISO 27001 project:
- Runs doctor diagnostic
- Checks critical risks
- Verifies control implementation progress
- Generates summary report
- Sends alerts if thresholds exceeded

Usage:
    python daily_check.py [--email ciso@example.com]

Setup with cron (daily at 8 AM):
    0 8 * * * /usr/bin/python3 /path/to/daily_check.py
"""

import subprocess
import sys
import json
from datetime import datetime
from pathlib import Path
import argparse
import smtplib
from email.message import EmailMessage

# Configuration
CRITICAL_RISK_THRESHOLD = 5
MIN_MATURITY_PERCENT = 75
REPORT_DIR = Path("reports/daily")


class ISO27001HealthCheck:
    """Daily health check for ISO 27001 project"""

    def __init__(self):
        self.report_date = datetime.now().strftime("%Y-%m-%d")
        self.report_time = datetime.now().strftime("%H:%M:%S")
        self.results = {
            "date": self.report_date,
            "time": self.report_time,
            "checks": [],
            "alerts": [],
            "status": "OK"
        }

    def run_command(self, cmd):
        """Execute CLI command and return output"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"ERROR: {e.stderr}"

    def check_doctor(self):
        """Run iso27001 doctor diagnostic"""
        print("1. Running doctor diagnostic...")
        output = self.run_command("iso27001 doctor")
        
        # Parse health score (simple extraction)
        if "Score de santé:" in output:
            try:
                score_line = [l for l in output.split('\n') if 'Score de santé:' in l][0]
                score = int(score_line.split(':')[1].split('%')[0].strip())
                
                self.results["checks"].append({
                    "name": "Doctor Diagnostic",
                    "status": "PASS" if score >= 80 else "WARNING",
                    "value": f"{score}%",
                    "threshold": "≥80%"
                })
                
                if score < 80:
                    self.results["alerts"].append(
                        f"Health score below 80%: {score}%"
                    )
            except:
                self.results["checks"].append({
                    "name": "Doctor Diagnostic",
                    "status": "ERROR",
                    "error": "Failed to parse health score"
                })
        
        return output

    def check_critical_risks(self):
        """Check number of critical risks"""
        print("2. Checking critical risks...")
        output = self.run_command("iso27001 risks list --level critical")
        
        # Count risks (simple line count)
        critical_count = len([l for l in output.split('\n') if 'RISK-' in l])
        
        self.results["checks"].append({
            "name": "Critical Risks",
            "status": "FAIL" if critical_count > CRITICAL_RISK_THRESHOLD else "PASS",
            "value": critical_count,
            "threshold": f"≤{CRITICAL_RISK_THRESHOLD}"
        })
        
        if critical_count > CRITICAL_RISK_THRESHOLD:
            self.results["alerts"].append(
                f"Too many critical risks: {critical_count} (threshold: {CRITICAL_RISK_THRESHOLD})"
            )
            self.results["status"] = "ALERT"
        
        return critical_count

    def check_control_maturity(self):
        """Check control implementation maturity"""
        print("3. Checking control maturity...")
        output = self.run_command("iso27001 controls list --format summary")
        
        # Parse maturity (this is a simplified version)
        # In reality, you'd parse the actual output format
        self.results["checks"].append({
            "name": "Control Maturity",
            "status": "INFO",
            "note": "See full report for details"
        })
        
        return output

    def generate_report(self):
        """Generate daily report"""
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        
        report_file = REPORT_DIR / f"health_check_{self.report_date}.txt"
        
        with open(report_file, 'w') as f:
            f.write(f"ISO 27001 Daily Health Check\n")
            f.write(f"{'=' * 50}\n")
            f.write(f"Date: {self.report_date} {self.report_time}\n\n")
            
            f.write("Checks:\n")
            for check in self.results["checks"]:
                status_symbol = {
                    "PASS": "✓",
                    "WARNING": "⚠",
                    "FAIL": "✗",
                    "ERROR": "!",
                    "INFO": "ℹ"
                }.get(check["status"], "?")
                
                f.write(f"  {status_symbol} {check['name']}: {check.get('value', 'N/A')}\n")
            
            if self.results["alerts"]:
                f.write("\nAlerts:\n")
                for alert in self.results["alerts"]:
                    f.write(f"  🚨 {alert}\n")
            
            f.write(f"\nOverall Status: {self.results['status']}\n")
        
        print(f"\n✓ Report saved: {report_file}")
        return report_file

    def send_email_alert(self, recipient):
        """Send email alert if issues detected"""
        if not self.results["alerts"]:
            print("No alerts to send")
            return
        
        msg = EmailMessage()
        msg['Subject'] = f"ISO 27001 Alert - {self.report_date}"
        msg['From'] = "iso27001-bot@example.com"
        msg['To'] = recipient
        
        body = f"""
ISO 27001 Daily Health Check - ALERTS DETECTED

Date: {self.report_date} {self.report_time}
Status: {self.results['status']}

Alerts:
"""
        for alert in self.results["alerts"]:
            body += f"  - {alert}\n"
        
        body += "\nPlease review the full report and take action.\n"
        msg.set_content(body)
        
        # NOTE: Configure your SMTP server here
        # with smtplib.SMTP('smtp.example.com', 587) as smtp:
        #     smtp.starttls()
        #     smtp.login('username', 'password')
        #     smtp.send_message(msg)
        
        print(f"📧 Email alert would be sent to {recipient}")
        print("    (SMTP configuration required)")

    def run(self, email=None):
        """Execute full health check"""
        print(f"\n📊 ISO 27001 Daily Health Check - {self.report_date}\n")
        
        self.check_doctor()
        self.check_critical_risks()
        self.check_control_maturity()
        
        report_file = self.generate_report()
        
        if email and self.results["alerts"]:
            self.send_email_alert(email)
        
        # Print summary
        print(f"\nSummary:")
        print(f"  Status: {self.results['status']}")
        print(f"  Alerts: {len(self.results['alerts'])}")
        print(f"  Report: {report_file}")
        
        # Exit with error code if alerts
        return 1 if self.results["alerts"] else 0


def main():
    parser = argparse.ArgumentParser(description="ISO 27001 Daily Health Check")
    parser.add_argument(
        '--email',
        help='Email address for alerts',
        default=None
    )
    args = parser.parse_args()
    
    checker = ISO27001HealthCheck()
    exit_code = checker.run(email=args.email)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
