document.addEventListener('DOMContentLoaded', function(){
    const sides = {
        "UA": "UA",
        "RU": "RU",
    }
    const pieChartCanvas = document.getElementById('pieChart').getContext('2d');
    const lineChartCanvas = document.getElementById('lineChart').getContext('2d');


    const sortedReportDates = getSortedReportDates(losses)
    const formattedLossesCounts = getFormattedLossesCounts(losses, sortedReportDates, sides)
    createSidesTotalLossesPieChart(pieChartCanvas, formattedLossesCounts, sides)
    createSidesAllLossesLineChart(lineChartCanvas, sides, formattedLossesCounts, 'total');
});

function createSidesAllLossesLineChart(canvas, sides, formattedLossesCounts, category) {
    const totalCategoryLoses = getAllTotalCategoryLosesForSides(formattedLossesCounts, category)
    new Chart(canvas, {
        type: 'line',
        data: {
            datasets: [{
                label: sides["UA"],
                data: totalCategoryLoses[sides["UA"]],
                borderColor: [
                    'rgb(54, 162, 235)',
                ],
                backgroundColor: 'rgb(0,122,210)',
                pointBorderColor: ['rgb(0,122,210)']
            },{
                label: sides["RU"],
                data: totalCategoryLoses[sides["RU"]],
                borderColor: [
                    'rgb(255, 99, 132)',
                ],
                backgroundColor: 'rgb(224,2,51)',
                pointBorderColor: ['rgb(224,2,51)']
            }]
        },
        options: {
            fill: false,
            borderWidth: 6,
            tension: 0.2,
            elements: {
                point: {
                    radius: 1,
                    hoverRadius: 6,
                    hitRadius: 6,
                }
            },
            scales: {
                x: {
                    type: 'time',
                    parsing: false,
                    time: {
                      unit: 'quarter',
                      displayFormats: {
                          quarter: 'MMM yyyy',
                          tooltipFormat:'MM/DD/YYYY'
                      }
                    },
                },
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        title: function(context) {
                            const label = context[0].label
                            return label.slice(0, label.lastIndexOf(','));
                        }
                    }
                }
            }
        },
    });
}

function createSidesTotalLossesPieChart(canvas, formattedLossesCounts, sides) {
        const loses = getLastTotalCategoryLosesForSides(formattedLossesCounts, 'total')
        new Chart(canvas, {
            type: 'pie',
            data: {
                labels: ['Ukraine', 'russia'],
                datasets: [{
                    data: [
                        loses[sides["UA"]], loses[sides["RU"]],
                    ],
                    backgroundColor: [
                        'rgb(54, 162, 235)',
                        'rgb(255, 99, 132)',
                    ],borderColor: [
                        '#f8f8f873',
                        '#f8f8f873',
                    ],
                    borderWidth: 2
                }]
            },
        });
    }

function getSortedReportDates(losses) {
    const reportDates = new Set()
    for (const loss of losses) {
        reportDates.add(loss['date_added'])
    }
    return [...reportDates].sort()
}

function getLastTotalCategoryLosesForSides(formattedLossesCounts, category) {
    const result = {}
    for (const side in formattedLossesCounts) {
        result[side] = formattedLossesCounts[side][formattedLossesCounts[side].length - 1]['counts'][category]
    }
    return result
}

function getAllTotalCategoryLosesForSides(formattedLossesCounts, category) {
    const result = {}
    for (const side in formattedLossesCounts) {
        result[side] = []
        for (const report of formattedLossesCounts[side]) {
            result[side].push({
                x: report['date_added'],
                y: report['counts'][category]
            })
        }
    }
    console.log(result);
    return result
}


function getFormattedLossesCounts(losses, sortedReportDates, sides) {
    let formattedLossesCounts = {};
    for (const side in sides) {
        formattedLossesCounts[side] = []
        let previousReportCounts = {}
        for (const reportDate of sortedReportDates) {
            const reportLosses = losses.filter(loss => loss['date_added'] === reportDate && loss['side'] === side);
            const reportCounts = {
                'date_added': new Date(reportDate).getTime(),
                'counts': {}
            }
            for (const loss of reportLosses) {
                const currentLossItemsCount = (loss.name.match(/\d+/g) || []).length;
                reportCounts.counts.total = currentLossItemsCount + getValueOrZero(reportCounts.counts.total);
                reportCounts.counts[loss['category']] = currentLossItemsCount + + getValueOrZero(reportCounts.counts[loss['category']])
            }
            for (const prevCountCategory in previousReportCounts) {
                reportCounts.counts[prevCountCategory] = previousReportCounts[prevCountCategory] + getValueOrZero(reportCounts.counts[prevCountCategory])
            }
            formattedLossesCounts[side].push(reportCounts)
            previousReportCounts = reportCounts.counts;
        }
    }
    formattedLossesCounts = addStartWarZeroCounts(formattedLossesCounts)
    return formattedLossesCounts
}

function getValueOrZero(field) {
    return !!field && field > 0 ? field : 0
}

function addStartWarZeroCounts(formattedLossesCounts) {
    for (const side in formattedLossesCounts) {
        const counts = {}
        for (const category in formattedLossesCounts[side][formattedLossesCounts[side].length - 1]['counts']) {
            counts[category] = 0
        }
        formattedLossesCounts[side].unshift({
            'date_added': new Date('2022-02-24').getTime(),
            'counts': counts
        })
    }
    return formattedLossesCounts
}

