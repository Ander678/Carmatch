document.getElementById("consultaForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const dni = document.getElementById("dni").value.trim();
    const ruc = document.getElementById("ruc").value.trim();
    const resultado = document.getElementById("resultado");
    resultado.innerHTML = "<p>🔄 Consultando datos...</p>";

    try {
        let url = `/api/consultar?dni=${encodeURIComponent(dni)}`;
        if (ruc) url += `&ruc=${encodeURIComponent(ruc)}`;

        const res = await fetch(url);
        const data = await res.json();

        if (data.error) {
            resultado.innerHTML = `<p style='color:red;'>❌ ${data.error}</p>`;
            return;
        }

        // --- HTML del vendedor ---
        let html = `
            <h3>👤 Datos del Vendedor</h3>
            <p><b>Nombre:</b> ${data.datosVendedor?.nombre || 'No disponible'}</p>
            <p><b>DNI:</b> ${data.datosVendedor?.numeroDocumento || 'No disponible'}</p>
        `;

        // --- Empresa (solo si existe y no es null) ---
        if (data.datosEmpresa && Object.keys(data.datosEmpresa).length > 0) {
            html += `
                <h3>🏢 Datos de la Empresa</h3>
                <p><b>Razón Social:</b> ${data.datosEmpresa?.nombre || 'No disponible'}</p>
                <p><b>RUC:</b> ${data.datosEmpresa?.numeroDocumento || 'No disponible'}</p>
                <p><b>Estado:</b> ${data.datosEmpresa?.estado || 'No disponible'}</p>
                <p><b>Condición:</b> ${data.datosEmpresa?.condicion || 'No disponible'}</p>
                <p><b>Dirección:</b> ${data.datosEmpresa?.direccion || 'No disponible'}</p>
            `;
        } else {
            html += `<p>⚠️ No se ingresó RUC o no se encontraron datos de empresa.</p>`;
        }

        // --- Botón de descarga de PDF ---
        html += `
            <form id="pdfForm" method="POST" action="/api/pdf" target="_blank">
                <input type="hidden" name="reporte" value='${JSON.stringify(data)}'>
                <button type="submit" style="
                    margin-top: 12px;
                    background-color: #007BFF;
                    color: white;
                    padding: 8px 14px;
                    border: none;
                    border-radius: 6px;
                    cursor: pointer;
                ">📄 Descargar PDF</button>
            </form>
        `;

        resultado.innerHTML = html;

    } catch (error) {
        console.error("Error al procesar respuesta:", error);
        resultado.innerHTML = `<p style='color:red;'>❌ Error al procesar respuesta: ${error.message}</p>`;
    }
});