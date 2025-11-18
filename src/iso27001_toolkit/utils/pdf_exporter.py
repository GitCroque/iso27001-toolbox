"""
Module d'export PDF pour ISO 27001

Fonctionnalités:
- Conversion Markdown → HTML → PDF
- Styling professionnel pour documents ISO 27001
- Support: politiques, SOA, registre risques, rapports audit
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

try:
    import markdown2
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

from iso27001_toolkit.logger import get_logger

logger = get_logger(__name__)


# CSS professionnel pour documents ISO 27001
ISO27001_CSS = """
@page {
    size: A4;
    margin: 2.5cm 2cm 2cm 2cm;

    @top-center {
        content: "ISO 27001:2022 - Document Confidentiel";
        font-size: 9pt;
        color: #666;
        font-family: Arial, sans-serif;
    }

    @bottom-right {
        content: "Page " counter(page) " / " counter(pages);
        font-size: 9pt;
        color: #666;
        font-family: Arial, sans-serif;
    }

    @bottom-left {
        content: "Généré le: {{ generation_date }}";
        font-size: 9pt;
        color: #666;
        font-family: Arial, sans-serif;
    }
}

body {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #333;
    text-align: justify;
}

h1 {
    color: #1a5490;
    font-size: 24pt;
    font-weight: bold;
    margin-top: 0;
    margin-bottom: 20pt;
    padding-bottom: 10pt;
    border-bottom: 3px solid #1a5490;
    page-break-after: avoid;
}

h2 {
    color: #2c5f8d;
    font-size: 18pt;
    font-weight: bold;
    margin-top: 20pt;
    margin-bottom: 12pt;
    page-break-after: avoid;
}

h3 {
    color: #3a6fa0;
    font-size: 14pt;
    font-weight: bold;
    margin-top: 15pt;
    margin-bottom: 10pt;
    page-break-after: avoid;
}

h4 {
    color: #4a7fb3;
    font-size: 12pt;
    font-weight: bold;
    margin-top: 12pt;
    margin-bottom: 8pt;
}

p {
    margin: 8pt 0;
    text-align: justify;
}

ul, ol {
    margin: 10pt 0;
    padding-left: 25pt;
}

li {
    margin: 5pt 0;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 15pt 0;
    font-size: 10pt;
    page-break-inside: avoid;
}

table thead {
    background-color: #1a5490;
    color: white;
    font-weight: bold;
}

table th {
    padding: 10pt;
    text-align: left;
    border: 1px solid #ddd;
}

table td {
    padding: 8pt;
    border: 1px solid #ddd;
}

table tbody tr:nth-child(even) {
    background-color: #f8f9fa;
}

table tbody tr:hover {
    background-color: #e9ecef;
}

code {
    background-color: #f4f4f4;
    padding: 2pt 5pt;
    border-radius: 3pt;
    font-family: 'Courier New', monospace;
    font-size: 9pt;
}

pre {
    background-color: #f4f4f4;
    padding: 10pt;
    border-radius: 5pt;
    border-left: 4px solid #1a5490;
    overflow-x: auto;
    page-break-inside: avoid;
}

pre code {
    background-color: transparent;
    padding: 0;
}

blockquote {
    border-left: 4px solid #ccc;
    padding-left: 15pt;
    margin: 15pt 0;
    color: #666;
    font-style: italic;
}

.cover-page {
    text-align: center;
    padding-top: 150pt;
    page-break-after: always;
}

.cover-page h1 {
    font-size: 32pt;
    color: #1a5490;
    margin-bottom: 30pt;
    border: none;
}

.cover-page .subtitle {
    font-size: 18pt;
    color: #666;
    margin: 20pt 0;
}

.cover-page .metadata {
    margin-top: 100pt;
    font-size: 12pt;
    color: #333;
}

.metadata-table {
    width: 100%;
    margin-bottom: 30pt;
    border: 2px solid #1a5490;
}

.metadata-table th {
    background-color: #1a5490;
    color: white;
    text-align: left;
}

.confidential-notice {
    background-color: #fff3cd;
    border: 2px solid #ffc107;
    padding: 15pt;
    margin: 20pt 0;
    border-radius: 5pt;
    text-align: center;
    font-weight: bold;
    color: #856404;
}

.risk-critical {
    background-color: #f8d7da;
    color: #721c24;
    font-weight: bold;
}

.risk-high {
    background-color: #fff3cd;
    color: #856404;
    font-weight: bold;
}

.risk-medium {
    background-color: #d1ecf1;
    color: #0c5460;
}

.risk-low {
    background-color: #d4edda;
    color: #155724;
}

.status-implemented {
    color: #28a745;
    font-weight: bold;
}

.status-in-progress {
    color: #ffc107;
    font-weight: bold;
}

.status-not-started {
    color: #dc3545;
    font-weight: bold;
}

.page-break {
    page-break-after: always;
}

.no-break {
    page-break-inside: avoid;
}

/* Footer disclaimer */
.footer-disclaimer {
    margin-top: 40pt;
    padding-top: 15pt;
    border-top: 1px solid #ccc;
    font-size: 9pt;
    color: #666;
    text-align: center;
}
"""


class PDFExporter:
    """
    Exporteur PDF pour documents ISO 27001

    Convertit des documents Markdown en PDF professionnels
    avec styling adapté pour la certification ISO 27001.
    """

    def __init__(self):
        """Initialise l'exporteur PDF"""
        if not WEASYPRINT_AVAILABLE:
            raise ImportError(
                "WeasyPrint et markdown2 sont requis pour l'export PDF.\n"
                "Installez-les avec: pip install weasyprint markdown2"
            )

        self.font_config = FontConfiguration()

    def _generate_cover_page(
        self,
        title: str,
        organization: str,
        document_type: str,
        metadata: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Génère une page de couverture HTML

        Args:
            title: Titre du document
            organization: Nom de l'organisation
            document_type: Type de document
            metadata: Métadonnées additionnelles

        Returns:
            HTML de la page de couverture
        """
        metadata = metadata or {}
        generation_date = datetime.now().strftime("%d/%m/%Y")

        metadata_rows = ""
        for key, value in metadata.items():
            metadata_rows += f"<tr><th>{key}</th><td>{value}</td></tr>\n"

        html = f"""
        <div class="cover-page">
            <h1>{title}</h1>
            <div class="subtitle">{document_type}</div>
            <div class="subtitle">{organization}</div>

            <div class="metadata">
                <table class="metadata-table">
                    <tr><th>Date de génération</th><td>{generation_date}</td></tr>
                    <tr><th>Type de document</th><td>{document_type}</td></tr>
                    <tr><th>Norme</th><td>ISO/IEC 27001:2022</td></tr>
                    {metadata_rows}
                </table>

                <div class="confidential-notice">
                    ⚠️ DOCUMENT CONFIDENTIEL ⚠️<br>
                    Ce document contient des informations confidentielles.<br>
                    Distribution restreinte - Usage interne uniquement.
                </div>
            </div>
        </div>
        """
        return html

    def _generate_footer_disclaimer(self, organization: str) -> str:
        """
        Génère le disclaimer de pied de page

        Args:
            organization: Nom de l'organisation

        Returns:
            HTML du disclaimer
        """
        year = datetime.now().year
        return f"""
        <div class="footer-disclaimer">
            <p>
                © {year} {organization} - Tous droits réservés<br>
                Document généré automatiquement par ISO 27001 Toolkit<br>
                Conforme à la norme ISO/IEC 27001:2022
            </p>
        </div>
        """

    def markdown_to_pdf(
        self,
        markdown_file: Path,
        output_pdf: Path,
        title: Optional[str] = None,
        organization: str = "Organisation",
        document_type: str = "Document ISO 27001",
        add_cover: bool = True,
        metadata: Optional[Dict[str, str]] = None,
        custom_css: Optional[str] = None
    ) -> Path:
        """
        Convertit un fichier Markdown en PDF

        Args:
            markdown_file: Fichier markdown source
            output_pdf: Fichier PDF de sortie
            title: Titre du document (déduit du fichier si non fourni)
            organization: Nom de l'organisation
            document_type: Type de document
            add_cover: Ajouter une page de couverture
            metadata: Métadonnées additionnelles pour la couverture
            custom_css: CSS personnalisé additionnel

        Returns:
            Path du fichier PDF généré
        """
        logger.info(f"Conversion PDF: {markdown_file} → {output_pdf}")

        # Lire le markdown
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Extraire le titre du markdown si non fourni
        if title is None:
            lines = markdown_content.split('\n')
            for line in lines:
                if line.startswith('# '):
                    title = line.replace('# ', '').strip()
                    break
            if title is None:
                title = markdown_file.stem

        # Convertir markdown → HTML
        html_body = markdown2.markdown(
            markdown_content,
            extras=[
                'tables',
                'fenced-code-blocks',
                'header-ids',
                'task_list',
                'strike',
                'code-friendly'
            ]
        )

        # Construire le HTML complet
        cover_html = ""
        if add_cover:
            cover_html = self._generate_cover_page(
                title=title,
                organization=organization,
                document_type=document_type,
                metadata=metadata
            )

        footer_html = self._generate_footer_disclaimer(organization)

        generation_date = datetime.now().strftime("%d/%m/%Y à %H:%M")
        css = ISO27001_CSS.replace("{{ generation_date }}", generation_date)
        if custom_css:
            css += f"\n{custom_css}"

        full_html = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <style>
                {css}
            </style>
        </head>
        <body>
            {cover_html}
            {html_body}
            {footer_html}
        </body>
        </html>
        """

        # Générer le PDF
        output_pdf.parent.mkdir(parents=True, exist_ok=True)

        HTML(string=full_html).write_pdf(
            output_pdf,
            font_config=self.font_config
        )

        logger.info(f"PDF généré avec succès: {output_pdf}")
        return output_pdf

    def export_policy_pdf(
        self,
        policy_file: Path,
        output_pdf: Path,
        organization: str = "Organisation"
    ) -> Path:
        """
        Exporte une politique en PDF

        Args:
            policy_file: Fichier markdown de la politique
            output_pdf: Fichier PDF de sortie
            organization: Nom de l'organisation

        Returns:
            Path du PDF généré
        """
        metadata = {
            "Catégorie": "Politique de sécurité",
            "Classification": "Confidentiel - Usage interne",
            "Version": "1.0"
        }

        return self.markdown_to_pdf(
            markdown_file=policy_file,
            output_pdf=output_pdf,
            organization=organization,
            document_type="Politique de Sécurité ISO 27001",
            metadata=metadata
        )

    def export_soa_pdf(
        self,
        soa_file: Path,
        output_pdf: Path,
        organization: str = "Organisation",
        maturity_score: Optional[float] = None
    ) -> Path:
        """
        Exporte le Statement of Applicability en PDF

        Args:
            soa_file: Fichier markdown du SoA
            output_pdf: Fichier PDF de sortie
            organization: Nom de l'organisation
            maturity_score: Score de maturité (optionnel)

        Returns:
            Path du PDF généré
        """
        metadata = {
            "Document": "Statement of Applicability (SoA)",
            "Norme": "ISO/IEC 27001:2022 - Annexe A",
            "Contrôles": "114 contrôles"
        }

        if maturity_score is not None:
            metadata["Score de maturité"] = f"{maturity_score:.1f}%"

        return self.markdown_to_pdf(
            markdown_file=soa_file,
            output_pdf=output_pdf,
            organization=organization,
            document_type="Statement of Applicability (SoA)",
            metadata=metadata
        )

    def export_risk_register_pdf(
        self,
        risk_file: Path,
        output_pdf: Path,
        organization: str = "Organisation",
        total_risks: Optional[int] = None
    ) -> Path:
        """
        Exporte le registre des risques en PDF

        Args:
            risk_file: Fichier markdown du registre
            output_pdf: Fichier PDF de sortie
            organization: Nom de l'organisation
            total_risks: Nombre total de risques (optionnel)

        Returns:
            Path du PDF généré
        """
        metadata = {
            "Document": "Registre des Risques",
            "Classification": "Confidentiel - Usage interne"
        }

        if total_risks is not None:
            metadata["Risques identifiés"] = str(total_risks)

        return self.markdown_to_pdf(
            markdown_file=risk_file,
            output_pdf=output_pdf,
            organization=organization,
            document_type="Registre des Risques ISO 27001",
            metadata=metadata
        )

    def export_audit_report_pdf(
        self,
        audit_file: Path,
        output_pdf: Path,
        organization: str = "Organisation",
        audit_date: Optional[str] = None
    ) -> Path:
        """
        Exporte un rapport d'audit en PDF

        Args:
            audit_file: Fichier markdown du rapport
            output_pdf: Fichier PDF de sortie
            organization: Nom de l'organisation
            audit_date: Date de l'audit (optionnel)

        Returns:
            Path du PDF généré
        """
        metadata = {
            "Type": "Rapport d'audit ISO 27001",
            "Classification": "Confidentiel - Diffusion restreinte"
        }

        if audit_date:
            metadata["Date d'audit"] = audit_date

        return self.markdown_to_pdf(
            markdown_file=audit_file,
            output_pdf=output_pdf,
            organization=organization,
            document_type="Rapport d'Audit ISO 27001",
            metadata=metadata
        )


def get_pdf_exporter() -> PDFExporter:
    """
    Récupère une instance de PDFExporter

    Returns:
        Instance de PDFExporter

    Raises:
        ImportError: Si WeasyPrint n'est pas disponible
    """
    return PDFExporter()


def check_pdf_support() -> bool:
    """
    Vérifie si l'export PDF est supporté

    Returns:
        True si WeasyPrint est disponible
    """
    return WEASYPRINT_AVAILABLE
