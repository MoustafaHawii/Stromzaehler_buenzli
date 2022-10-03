function getData(n, amp = 100) {
	const arr = [];
	let a, b, c;
	let x = Date.UTC(new Date().getUTCFullYear(), 0, 1) - n * 36e5;
	for (let i = 0; i < n; i++, x += 36e5) {
		if (i % 100 === 0) a = 2 * Math.random();
		if (i % 1000 === 0) b = 2 * Math.random();
		if (i % 10000 === 0) c = 2 * Math.random();
		const spike = i % 50000 === 0 ? 10 : 0;
		arr.push([
			x,
			2 * Math.sin(i / amp) + a + b + c + spike + Math.random(),
		]);
	}
	return arr;
}
const n = 500000;
const data = getData(n);
const data2 = getData(n, 200);
console.time("line");
const chart = Highcharts.stockChart("container", {
	chart: {
		zoomType: "x",
	},
	title: {
		text: "Stromzähler",
	},
	rangeSelector: {
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
	series: [
		{
			name: "Einspeisung",
			data: data,
		},
		{
			name: "Verbrauch",
			data: data2,
		},
	],
	exporting: {
		buttons: [
			{
				text: "month >",
				onclick: () => {
					translateChart((date) =>
						date.setMonth(date.getMonth() + 1)
					);
				},
			},
			{
				text: "day >",
				onclick: () => {
					translateChart((date) => date.setDate(date.getDate() + 1));
				},
			},
			{
				text: "< day",
				onclick: () => {
					translateChart((date) => date.setDate(date.getDate() - 1));
				},
			},
			{
				text: "< month",
				onclick: () => {
					translateChart((date) =>
						date.setMonth(date.getMonth() - 1)
					);
				},
			},
		],
	},
});

function translateChart(changeFn) {
	const { min, max } = chart.xAxis[0].getExtremes();
	chart.xAxis[0].setExtremes(
		changeFn(new Date(min)),
		changeFn(new Date(max))
	);
}

console.timeEnd("line");
