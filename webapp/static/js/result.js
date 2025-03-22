let resultsLoaded = false;

const floralMetalPalette = [
    '#ffb7c5', '#b0eacd', '#c8b4e3', '#b76e79', '#7da87b',
    '#f7e7ce', '#cd7f32', '#a8c5ff', '#f2e394', '#b87333'
];

function displayResults(data) {
    if (data.results.length > 0) {
        const topResult = data.results[0];

        document.getElementById("scientific-name").textContent = topResult.scientific_name;
        document.getElementById("popular-name").textContent = topResult.popular_name;
        document.getElementById("verification-link").href = topResult.link;
        document.getElementById("verification-link").textContent = "Ver mais";

        if (data.image_url) {
            document.getElementById("plant-image").src = data.image_url;
            document.getElementById("plant-image").style.display = "block";
        }
    }

    const ctx = document.getElementById('classificationChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.results.map(item => item.scientific_name),
            datasets: [{
                data: data.results.map(item => parseFloat(item.probability.replace('%', ''))),
                backgroundColor: data.results.map((_, i) => floralMetalPalette[i % floralMetalPalette.length]),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: {
                            family: 'Poppins'
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.raw}%`;
                        }
                    }
                }
            }
        }
    });
}

function updateResults() {
    if (resultsLoaded) {
        return;
    }

    fetch("/classification-results")
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro ao buscar os resultados da classificação");
            }
            return response.json();
        })
        .then(data => {
            if (!data || data.error) {
                console.error("Nenhuma classificação encontrada.");
                return;
            }
            displayResults(data);
            resultsLoaded = true;
        })
        .catch(error => console.error("Erro ao carregar dados da classificação:", error));
}

document.addEventListener("DOMContentLoaded", function () {
    const dataElement = document.getElementById('initial-data');
    const data = {
        results: JSON.parse(dataElement.dataset.results),
        imageUrl: dataElement.dataset.imageUrl
    };

    const ctx = document.getElementById('classificationChart').getContext('2d');

    // Ordenar os resultados por probabilidade decrescente
    const sortedResults = [...data.results].sort((a, b) => {
        return parseFloat(b.probability.replace('%', '')) - parseFloat(a.probability.replace('%', ''));
    });

    const labels = sortedResults.map(item => item.scientific_name);
    const probabilities = sortedResults.map(item => parseFloat(item.probability.replace('%', '')));

    // Cores principais por ordem de confiança
    const highlightColors = ['#7da87b', '#ffb7c5', '#c8b4e3']; // verde, rosa, lavanda

    // Cores extras da paleta floral/metálica
    const extraPalette = [
        '#b76e79', '#f7e7ce', '#cd7f32', '#a8c5ff', '#f2e394', '#b87333'
    ];

    // Combinar as cores principais com as extras, de acordo com o número de classes
    const finalColors = labels.map((_, i) => {
        return i < highlightColors.length
            ? highlightColors[i]
            : extraPalette[(i - highlightColors.length) % extraPalette.length];
    });

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: probabilities,
                backgroundColor: finalColors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: {
                            family: 'Poppins'
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.raw}%`;
                        }
                    }
                }
            }
        }
    });

    console.log('Dados do gráfico (ordenados):', {
        labels: labels,
        probabilities: probabilities,
        colors: finalColors
    });
});
