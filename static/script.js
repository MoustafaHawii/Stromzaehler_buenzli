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
				text: "Next Day",
				onclick: () => {
					const addDay = (ts) => {
						const date = new Date(ts);
						date.setDate(date.getDate() + 1);
						return date.getTime();
					};
					const { min, max } = chart.xAxis[0].getExtremes();
					chart.xAxis[0].setExtremes(addDay(min), addDay(max));
				},
				theme: {
					"stroke-width": 1,
					stroke: "silver",
					states: {
						hover: {
							fill: "#a4edba",
						},
						select: {
							stroke: "#039",
							fill: "#a4edba",
						},
					},
				},
			},
		],
	},
});
console.timeEnd("line");
