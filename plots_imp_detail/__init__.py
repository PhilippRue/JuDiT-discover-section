import panel as pn

show_empty_atoms= False


radius_impcls = 4.5 # Ang.


# initial value
old_impname = None



spinner_text = """
<!-- https://www.w3schools.com/howto/howto_css_loader.asp -->
<div class="loader">
<style scoped>
.loader {
    border: 16px solid #f3f3f3; /* Light grey */
    border-top: 16px solid #3498db; /* Blue */
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 2s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
} 
</style>
</div>
"""


footer = pn.pane.Markdown("""
Database version: XXXXX

[© Quantum Theory of Materials (PGI-1 / IAS-1)](https://www.fz-juelich.de/pgi/pgi-1/EN/Home/home_node.html)
""")

