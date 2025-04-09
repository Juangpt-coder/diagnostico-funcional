from zipfile import ZipFile
import os

# Crear carpeta temporal del proyecto
project_folder = "/mnt/data/diagnostico-funcional"
os.makedirs(project_folder, exist_ok=True)

# Guardar el archivo index.html con el contenido proporcionado
index_html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Diagnóstico Clínico Funcional</title>
  <link rel="manifest" href="/manifest.json" />
  <meta name="theme-color" content="#2c3e50" />
  <style>
    body {
      font-family: sans-serif;
      padding: 2rem;
      background: #f7f7f7;
      max-width: 600px;
      margin: auto;
    }
    h1 {
      color: #2c3e50;
    }
    textarea, button {
      width: 100%;
      padding: 1rem;
      margin: 1rem 0;
      font-size: 1rem;
      box-sizing: border-box; /* Added for better width handling */
    }
    .result {
      background: #ecf0f1;
      padding: 1rem;
      border-radius: 8px;
      margin-top: 1rem; /* Added margin */
    }
  </style>
</head>
<body>
  <h1>🩺 Diagnóstico Clínico Funcional con IA</h1>
  <p>Describe los síntomas principales del paciente:</p>
  <textarea id="sintomas" rows="4" placeholder="Ej. fatiga crónica, cefalea..."></textarea>
  <button onclick="diagnosticar()">Obtener diagnóstico</button>

  <div id="resultado" class="result" style="display:none;"></div>

  <script>
    async function diagnosticar() {
      const sintomasInput = document.getElementById("sintomas");
      const sintomas = sintomasInput.value.toLowerCase().trim(); // Added trim()
      const resultadoDiv = document.getElementById("resultado");

      // Clear previous results and show loading indicator (optional)
      resultadoDiv.innerHTML = "Procesando...";
      resultadoDiv.style.display = "block";

      if (!sintomas) {
          resultadoDiv.innerHTML = "Por favor, describe los síntomas.";
          return; // Stop if no symptoms entered
      }

      // More robust symptom matching (can be expanded)
      const diagnosticos = {
        "dolor abdominal": "Síndrome de intestino irritable",
        "abdomen": "Síndrome de intestino irritable", // Alias
        "estómago": "Síndrome de intestino irritable", // Alias
        "fatiga crónica": "Disbiosis intestinal",
        "cansancio": "Disbiosis intestinal", // Alias
        "fatiga": "Disbiosis intestinal", // Alias
        "dolor articular": "Inflamación sistémica",
        "articulaciones": "Inflamación sistémica", // Alias
        "cefalea": "Sensibilidad al gluten o histamina",
        "dolor de cabeza": "Sensibilidad al gluten o histamina", // Alias
        "cabeza": "Sensibilidad al gluten o histamina", // Alias
        "insomnio": "Desregulación del eje HHA",
        "dormir": "Desregulación del eje HHA" // Alias
      };

      const recomendaciones = {
        "Síndrome de intestino irritable": [
          "Eliminar gluten, lácteos y azúcares refinados",
          "Probióticos (Lactobacillus plantarum, Bifidobacterium infantis)",
          "Dieta baja en FODMAPs (bajo supervisión profesional)",
          "Suplementación con L-glutamina"
        ],
        "Disbiosis intestinal": [
          "Probióticos y prebióticos (fibra soluble e insoluble)",
          "Evitar antibióticos innecesarios",
          "Dieta rica en fibra vegetal variada",
          "Considerar berberina o extractos antimicrobianos naturales (con guía)"
        ],
        "Inflamación sistémica": [
          "Aumentar consumo de Omega 3 (pescado azul, semillas de chía/lino) o suplementar EPA/DHA",
          "Optimizar niveles de Vitamina D3 (exposición solar segura o suplementación)",
          "Dieta antiinflamatoria (rica en vegetales, frutas, grasas saludables; baja en procesados)",
          "Considerar curcumina, resveratrol u otros polifenoles"
        ],
        "Sensibilidad al gluten o histamina": [
          "Eliminar gluten estrictamente (si aplica)",
          "Dieta baja en histamina (evitar fermentados, curados, alcohol, tomate, espinacas...)",
          "Considerar suplementación con DAO (diamina oxidasa) antes de las comidas",
          "Usar quercetina como estabilizador de mastocitos"
        ],
        "Desregulación del eje HHA": [
          "Considerar melatonina (dosis bajas: 0.5-3mg) si hay dificultad para dormir",
          "Adaptógenos como ashwagandha, rhodiola (evaluar individualmente)",
          "Higiene del sueño: evitar pantallas antes de dormir, oscuridad total",
          "Ejercicio físico regular (preferiblemente por la mañana), manejo del estrés (mindfulness, yoga)"
        ]
      };

      let diagnostico = "Diagnóstico no definido con la información proporcionada.";
      let recs = [];
      let found = false; // Flag to stop after first match

      // Improved matching: check if any key *is contained within* the symptoms string
      for (const clave in diagnosticos) {
        if (sintomas.includes(clave)) {
          diagnostico = diagnosticos[clave];
          recs = recomendaciones[diagnostico] || []; // Ensure recs is always an array
          found = true;
          break; // Stop searching once a match is found
        }
      }

       // Use a default message if no specific diagnosis was found
      if (!found) {
           diagnostico = "No se pudo determinar un diagnóstico específico con los síntomas proporcionados. Se recomienda consulta profesional.";
           recs = [
                "Mantener una dieta equilibrada y variada.",
                "Asegurar un descanso adecuado.",
                "Realizar actividad física moderada.",
                "Consultar con un profesional de la salud para una evaluación completa."
           ];
      }

      // Simulate fetching evidence (replace with actual API call if needed)
      const evidencia = await obtenerEvidencia(found ? diagnostico : "Salud general"); // Fetch general evidence if no diagnosis

      let html = `<strong>🧠 Diagnóstico Sugerido:</strong> ${diagnostico}<br/><br/>`;
      if (recs.length > 0) {
        html += `<strong>🧾 Recomendaciones Funcionales:</strong><ul>`;
        recs.forEach(r => html += `<li>${r}</li>`);
        html += `</ul><br/>`; // Added line break
      }

      html += `<strong>📚 Posibles Fuentes de Evidencia (Ejemplos):</strong><ul>`;
      evidencia.forEach(ref => html += `<li>${ref}</li>`);
      html += `</ul><br/>`; // Added line break

      html += `<p style="font-size: 0.8em; color: #555;"><i>Nota: Esta herramienta es solo una guía inicial y no reemplaza la consulta médica profesional.</i></p>`;


      resultadoDiv.innerHTML = html;
      // No need to set display:block again if already set
    }

    // Mock function for fetching evidence
    async function obtenerEvidencia(terminoBusqueda) {
       // In a real app, you might fetch from an API based on 'terminoBusqueda'
       // For now, just return static examples potentially related
       console.log("Buscando evidencia para:", terminoBusqueda); // For debugging
       await new Promise(resolve => setTimeout(resolve, 150)); // Simulate network delay

       const fuentes = [
        `[PubMed] Búsqueda de estudios: "${terminoBusqueda}" + "functional medicine"`,
        `[Epistemonikos] Búsqueda de revisiones sistemáticas: "${terminoBusqueda}"`,
        `[Cochrane Library] Búsqueda de meta-análisis: "${terminoBusqueda}" + "nutrition"`,
        `[Doctomatic] Explorar guías clínicas interactivas relacionadas con "${terminoBusqueda}"`
      ];
      // Add more specific examples if needed based on terminoBusqueda
      if (terminoBusqueda === "Síndrome de intestino irritable") {
          fuentes.push("[PubMed] Estudio sobre dieta baja en FODMAPs y SII");
      }
      if (terminoBusqueda === "Disbiosis intestinal") {
          fuentes.push("[PubMed] Meta-análisis sobre probióticos para disbiosis");
      }
       // Add more specific examples if needed...

      return fuentes;
    }

    // Optional: Add listener for Enter key in textarea
    document.getElementById("sintomas").addEventListener("keypress", function(event) {
        if (event.key === "Enter" && !event.shiftKey) { // Allow Shift+Enter for new lines
            event.preventDefault(); // Prevent default Enter behavior (new line)
            diagnosticar(); // Trigger diagnosis
        }
    });

    // Optional: Register Service Worker (if you create sw.js and manifest.json)
    /*
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').then(registration => {
          console.log('SW registered: ', registration);
        }).catch(registrationError => {
          console.log('SW registration failed: ', registrationError);
        });
      });
    }
    */
  </script>
</body>
</html>
"""

# Write index.html ensuring UTF-8 encoding
index_file_path = os.path.join(project_folder, "index.html")
with open(index_file_path, "w", encoding="utf-8") as f:
    f.write(index_html_content.strip()) # Use strip() to remove leading/trailing whitespace

# Crear vercel.json
vercel_config = """
{
  "cleanUrls": true,
  "rewrites": [
    { "source": "/", "destination": "/index.html" }
  ]
}
"""
# Note: Using the original rewrite rule as provided by the user in the last prompt.

vercel_file_path = os.path.join(project_folder, "vercel.json")
with open(vercel_file_path, "w", encoding="utf-8") as f: # Added encoding for consistency
    f.write(vercel_config.strip()) # Use strip()

# Comprimir todo
zip_path = "/mnt/data/diagnostico-funcional.zip"
print(f"Creando archivo zip en: {zip_path}")

with ZipFile(zip_path, "w") as zipf:
    # Walk through the directory
    for root, dirs, files in os.walk(project_folder):
        for file in files:
            # Create the full path to the file
            file_path = os.path.join(root, file)
            # Create the relative path for the archive
            # This ensures files are stored like 'index.html', not '/mnt/data/diagnostico-funcional/index.html'
            arcname = os.path.relpath(file_path, project_folder)
            print(f"  Añadiendo: {arcname}")
            # Add file to the zip
            zipf.write(file_path, arcname)

print(f"Archivo zip '{zip_path}' creado exitosamente.")

# Devolver la ruta del archivo zip generado
zip_path