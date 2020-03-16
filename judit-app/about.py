import markdown
import panel as pn
from global_settings import website_width, DOI_DATABASE_MC_ARCHIVE

judit_header = pn.Column(
    pn.Row(
        pn.pane.PNG("judit-app/images/JuDiT_logo_round.png", width=400),
        pn.pane.HTML("<img  align='right' src='https://www.fz-juelich.de/SiteGlobals/StyleBundles/Bilder/NeuesLayout/logo.jpg?__blob=normal' href='www.fz-juelich.de' width='200'/>"
                    ""
                    "\n"
                    ""
                    , width=website_width),
    ),
    pn.pane.Markdown("## **Jü**lich **D**atabase of **i**mpurities embedded into a **T**opological insulator"
                , width=website_width),
    pn.pane.LaTeX("A collection first principles calculations for impurities embedded into the strong topological insulator Sb$_2$Te$_3$."
                , width=website_width),
    pn.pane.HTML("<br></br>"
                 "<div align='right'>"
                +"    <a href'https://archive.materialscloud.org'>Database version: v1.0</a>"
                +"    <p> doi: {}</p>".format(DOI_DATABASE_MC_ARCHIVE)
                +"</div>"
                , width=website_width),
                
)



how_to_cite = (
    "### If you use this tool please cite the following publication:\n"
    "\n"
    "#### Philipp Rüßmann, Fabian Bertoldo, and Stefan Blügel, *The AiiDA-KKR plugin and its application to high-throughput impurity embedding into a topological insulator*, in preparation (2020)."
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

)



how_to_cite = pn.pane.Markdown(how_to_cite, width=800, sizing_mode='stretch_both')

about = pn.pane.Markdown(about, width=800, sizing_mode='stretch_both')

acknowledgements = pn.pane.Markdown(acknowledgements, width=800, sizing_mode='stretch_both')

used_software = pn.pane.Markdown(used_software, width=800, sizing_mode='stretch_both')

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
                     +"\n"
                     +"* [Forschungszentrum Jülich](https://www.fz-juelich.de/portal/DE/Home/home_node.html)\n"
                     +"* [Institute for Advanced Simulation (IAS-1)](https://www.fz-juelich.de/pgi/pgi-1/DE/Home/home_node.html)\n"
                     +"* [Institute Quantum Theory of Materials (PGI-1)](https://www.fz-juelich.de/pgi/pgi-1/DE/Home/home_node.html)\n"
                     +"* [juDFT: DFT codes from Forschungszentrum Jülich](http://www.judft.de)\n"
                     +"* [juKKR: The Jülich KKR codes](https://jukkr.fz-juelich.de)\n"
                     +"* [AiiDA](http://www.aiida.net)\n"
                     +"* [MaterialsCloud](https://www.materialscloud.org)\n"
                     +"\n"
                     +"[Contact: Dr. Philipp Rüßmann](mailto:p.ruessmann@fz-juelich.de?subject=[JuDiT])\n\n"
                     +"[©2020 Quantum Theory of Materials (PGI-1 / IAS-1)](https://www.fz-juelich.de/pgi/pgi-1/EN/Home/home_node.html)\n"
                     +"</small>\n"
                    , width=website_width))
