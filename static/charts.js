var chartDataRaw;
var chartData = {};

// fetch data from server
fetch("/static/data.json")
	.then((response) => response.json())
	.then((data) => {
		chartDataRaw = data;
		chartData["relative"] = {};
		chartData["absolute"] = {};

		const relative = { feed: [], usg: [] };
		const absolute = { feed: [], usg: [] };

		for (const entry of data) {
			const ts = new Date(entry.ts).getTime();
			relative["feed"].push([ts, entry.feedR]);
			relative["usg"].push([ts, entry.usgR]);
			absolute["feed"].push([ts, Math.max(entry.feedA, 0)]);
			absolute["usg"].push([ts, Math.max(entry.usgA, 0)]);
		}
		chartData = { relative, absolute };
		setView(0);
	})
	.catch((error) => {
		console.log(error);
	});

/**
 * Updates the chart view
 * @param {number} viewIndex the view index to switch to
 * (0 - relative, 1 - absolute)
 */
function setView(viewIndex) {
	if (viewIndex) {
		const data = chartData.absolute;
		updateSeries(data.feed, data.usg);
	} else {
		const data = chartData.relative;
		updateSeries(data.feed, data.usg);
	}
}

/**
 * updates the chart series
 * @param  {...any} newData new chart data
 */
function updateSeries(...newData) {
	const names = chart.series.map((s) => s.name);
	while (!!chart.series.length) {
		chart.series[0].remove();
	}
	for (const data of newData) {
		chart.addSeries({ name: names.shift(), data });
	}
}

const chart = Highcharts.stockChart("container", {
	chart: {
		zoomType: "x",
		panKey: "shift",
		panning: {
			enabled: true,
			type: "x",
		},
	},
	title: {
		text: "Stromzähler",
	},
	rangeSelector: {
		floating: true,
		buttons: [
			{
				type: "day",
				count: 1,
				text: "1d",
			},
			{
				type: "week",
				count: 1,
				text: "1w",
			},
			{
				type: "month",
				count: 1,
				text: "1m",
			},
			{
				type: "month",
				count: 6,
				text: "6m",
			},
			{
				type: "year",
				count: 1,
				text: "1y",
			},
			{
				type: "all",
				text: "All",
			},
		],
		selected: 2,
	},
	series: [{ name: "Einspeisung" }, { name: "Verbrauch" }],
	exporting: {
		buttons: {
			contextButton: {
				menuItems: [
					{
						textKey: "printChart",
						onclick: function () {
							this.print();
						},
					},
					{
						separator: true,
					},
					{
						text: "Import XML",
						onclick: function () {
							document.querySelector("#file-input").click();
							document
								.querySelector("#file-input")
								.addEventListener("change", () => {
									document
										.querySelector("#submit-btn")
										.click();
								});
						},
					},
					{
						text: "Download CSV",
						onclick: function () {
							download("data.csv", jsonToCSV(chartDataRaw));
						},
					},
					{
						text: "Download JSON",
						onclick: function () {
							download(
								"data.json",
								JSON.stringify(chartDataRaw, null, 4)
							);
						},
					},
					{
						separator: true,
					},
					{
						textKey: "downloadPNG",
						onclick: function () {
							this.exportChart();
						},
					},
					{
						textKey: "downloadJPEG",
						onclick: function () {
							this.exportChart({
								type: "image/jpeg",
							});
						},
					},
					{
						separator: true,
					},
					{
						textKey: "downloadPDF",
						onclick: function () {
							this.exportChart({
								type: "application/pdf",
							});
						},
					},
					{
						textKey: "downloadSVG",
						onclick: function () {
							this.exportChart({
								type: "image/svg+xml",
							});
						},
					},
				],
			},
			nextMonth: {
				text: "month +",
				onclick: () => {
					translateChart((date) =>
						date.setMonth(date.getMonth() + 1)
					);
				},
			},
			nextDay: {
				text: "day +",
				onclick: () => {
					translateChart((date) => date.setDate(date.getDate() + 1));
				},
			},
			prevDay: {
				text: "- day",
				onclick: () => {
					translateChart((date) => date.setDate(date.getDate() - 1));
				},
			},
			prevMonth: {
				text: "- month",
				onclick: () => {
					translateChart((date) =>
						date.setMonth(date.getMonth() - 1)
					);
				},
			},
			toggle: {
				text: "Toggle view",
				onclick: () => {
					alert("toggling");
				},
				align: "left",
			},
		},
	},
	navigation: {
		buttonOptions: {
			align: "right",
		},
	},
	legend: {
		enabled: true,
	},
	tooltip: {
		formatter: function () {
			return this.points.reduce(function (s, point) {
				return `${s}<br/>${point.series.name} : ${point.y} kWh`;
			}, "<b>" + new Date(this.x).toLocaleString() + "</b>");
		},
	},
});

/**
 * Translates the chart horizontally
 * @param {Function} changeFn
 * function that modifies the dateobj
 */
function translateChart(changeFn) {
	const { min, max } = chart.xAxis[0].getExtremes();
	chart.xAxis[0].setExtremes(
		changeFn(new Date(min)),
		changeFn(new Date(max))
	);
}

const select = Highcharts.createElement(
	"select",
	{
		onchange: function () {
			setView(this.selectedIndex);
		},
	},
	{
		position: "absolute",
		top: "20px",
		left: "10px",
	},
	document.querySelector("#container")
);

["relative Werte", "absolute Werte"].forEach(function (element) {
	Highcharts.createElement(
		"option",
		{
			value: element,
			innerHTML: element,
		},
		{},
		select
	);
});
