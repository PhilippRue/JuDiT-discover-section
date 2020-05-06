import markdown
import panel as pn
from global_settings import website_width, DOI_DATABASE_MC_ARCHIVE

judit_header = pn.Column(
    pn.Row(
        pn.pane.PNG("judit-app/images/JuDiT_logo_round.png", width=400),
        pn.Spacer(width=website_width-600),
        pn.Column(
            pn.Spacer(height=10),
            pn.pane.PNG("judit-app/images/fz_logo.png", width=200, align='end'),
            pn.Spacer(height=10),
            pn.pane.PNG("judit-app/images/jl-vmd-logo.png", width=200, align='end'),
            pn.Spacer(height=10),
            align='end',
        ),
    ),
    pn.pane.Markdown("## **Jü**lich **D**atabase of **i**mpurities embedded into a **T**opological insulator"
                , width=website_width),
    pn.pane.LaTeX("A collection first principles calculations for impurities embedded into the strong topological insulator Sb$_2$Te$_3$."
                , width=website_width),
    pn.pane.HTML("<br></br>"
                 "<div align='right'>"
                +"    <a href='https://archive.materialscloud.org/2020.0030/v1'>Database version: v1.0</a>"
                +"    <p><a href='https://doi.org/{0}'> doi: {0}</a></p>".format(DOI_DATABASE_MC_ARCHIVE)
                +"</div>"
                , width=website_width),
)
                




how_to_cite = (
    "### If you use this tool please cite the following publication:\n"
    "\n"
    "Philipp Rüßmann, Fabian Bertoldo, and Stefan Blügel, *The AiiDA-KKR plugin and its application to high-throughput impurity embedding into a topological insulator*, [arXiv:2003.08315 [cond-mat.mtrl-sci] (2020)](https://arxiv.org/abs/2003.08315)."
    "\n"
    "### Please also cite the data set:"
    "\n"
    "Philipp Rüßmann, Fabian Bertoldo, Stefan Blügel, *The JuDiT database of impurities embedded into a Topological Insulator*, Materials Cloud Archive (2020), [doi: {0}](https://doi.org/{0}).".format(DOI_DATABASE_MC_ARCHIVE)
)

about = markdown.markdown(
    "We present the development of the AiiDA-KKR plugin that allows to perform a large number of \n"
    "*ab initio* impurity embedding calculations based on the relativistic full-potential \n"
    "Korringa-Kohn-Rostoker Green function method.\n"
    "The capabilities of the AiiDA-KKR plugin are demonstrated with the calculation of several \n"
    "thousand impurities embedded into the prototypical topological insulator Sb2Te3.\n"
    "The results are collected in the JuDiT database which we use to investigate chemical trends \n"
    "as well as Fermi level and layer dependence of physical properties of impurities. \n"
    "This includes the study of spin moments, the impurity's tendency to form in-gap states or its \n"
    "effect on the charge doping of the host-crystal.\n"
    "These properties depend on the detailed electronic structure of the impurity embedded into the \n"
    "host crystal which highlights the need for *ab initio* calculations in order to get accurate \n"
    "predictions."
)

acknowledgements = markdown.markdown(
    "### Computational support\n"
    "\n"
    "Computing time for this project was granted by the JARA Vergabegremium and \n"
    "provided on the JARA Partition part of the supercomputer CLAIX at RWTH Aachen University.\n"
    "\n"
    "### Funding\n"
    "\n"
    "We acknowledge funding from the Priority Programme SPP-1666 Topological Insulators \n"
    "of the Deutsche Forschungs- gemeinschaft (DFG) (projects MA4637/3-1), from the \n"
    "VITI Programme of the Helmholtz Association, as well as the\n" 
    "Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) \n"
    "under Germany's Excellence Strategy - Cluster of Excellence Matter \n"
    "and Light for Quantum Computing (ML4Q) EXC 2004/1 - 390534769.\n"
    "Furthermore, this work was supported by the MaX Center of Excellence funded by the EU \n"
    "through the H2020-EINFRA-2015-1 project: GA 676598 as well as by the \n"
    "Joint Lab Virtual Materials Design (JLVMD) of the Forschungszentrum Jülich."
)

used_software = markdown.markdown(
    "### Software\n"
    "\n"
    "- aiida-core: [www.aiida.net](www.aiida.net)\n"
    "- masci-tools: [https://github.com/JuDFTteam/masci-tools](https://github.com/JuDFTteam/masci-tools)\n"
    "- ase-notebook: [https://github.com/chrisjsewell/ase-notebook](https://github.com/chrisjsewell/ase-notebook)\n"
    "- bokeh: [https://bokeh.org](https://bokeh.org)\n"
    "- panel: [https://panel.holoviz.org](https://panel.holoviz.org)\n"

)



how_to_cite = pn.pane.Markdown(how_to_cite, width=website_width, sizing_mode='stretch_both')

about = pn.pane.Markdown(about, width=website_width, sizing_mode='stretch_both')

acknowledgements = pn.pane.Markdown(acknowledgements, width=website_width, sizing_mode='stretch_both')

used_software = pn.pane.Markdown(used_software, width=website_width, sizing_mode='stretch_both')

db_info = pn.Tabs(('How to cite', how_to_cite), 
                  ('About the databse', about), 
                  ('Acknowledgements', acknowledgements),
                  ('Used software', used_software)
                 )




judit_footer = pn.Column(
    pn.pane.Markdown("---\n"
                     +"<small>\n"
                     +"\n"
                     +"\n"
                     +"### Links\n"
                     +"</small>"),
    pn.Row(
        pn.pane.Markdown("<small>\n"
                        +"\n"
                        +"* [Forschungszentrum Jülich](https://www.fz-juelich.de/portal/DE/Home/home_node.html)\n"
                        +"* [Institute for Advanced Simulation (IAS-1)](https://www.fz-juelich.de/pgi/pgi-1/DE/Home/home_node.html)\n"
                        +"* [Institute Quantum Theory of Materials (PGI-1)](https://www.fz-juelich.de/pgi/pgi-1/DE/Home/home_node.html)\n"
                        +"* [juDFT: DFT codes from Forschungszentrum Jülich](http://www.judft.de)\n"
                        +"\n"
                        +"</small>\n"),
        pn.pane.Markdown("<small>\n"
                        +"\n"
                        +"* [Joint Lab - Virtual Materials Design](https://www.fz-juelich.de/pgi/pgi-1/EN/Forschung/Joint-Lab-VMD/artikel.html)\n"
                        +"* [juKKR: The Jülich KKR codes](https://jukkr.fz-juelich.de)\n"
                        +"* [AiiDA](http://www.aiida.net)\n"
                        +"* [MaterialsCloud](https://www.materialscloud.org)\n"
                        +"\n"
                        +"</small>\n"),
    ),
    pn.pane.Markdown("<small>\n"
                     +"\n"
                     +"[Contact: Dr. Philipp Rüßmann](mailto:p.ruessmann@fz-juelich.de?subject=[JuDiT])\n\n"
                     +"[©2020 Quantum Theory of Materials (PGI-1 / IAS-1)](https://www.fz-juelich.de/pgi/pgi-1/EN/Home/home_node.html)\n"
                     +"</small>\n"),
    width=website_width,
)


def provenance_link(uuid, label=None):
    """
    Return representation of provenance link.

    Copied from discover section of curated cofs
    https://github.com/lsmo-epfl/discover-curated-cofs/blob/b30e33a1114f541dc0aeee22e8b15c2fc47aaf7c/select-figure/main.py#L22
    """
    import os

    if label is None:
        label = "Browse provenance\n" + str(uuid)

    logo_url = "judit-app/images/aiida-128.png"
    explore_url = os.getenv('EXPLORE_URL', "https://dev-www.materialscloud.org/explore/judit")

    return "<a href='{url}/details/{uuid}' target='_blank'><img src={logo_url} title='{label}' style='width: 20px;  height: auto;'></a>".format(  # noqa
        url=explore_url, uuid=str(uuid), label=label, logo_url=logo_url)
