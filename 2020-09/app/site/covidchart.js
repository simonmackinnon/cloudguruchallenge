function getColumn(arr, n) {
    return (arr, n) => arr.map(x => x[n])
}

function compare( a, b ) {
  if ( a.date < b.date ){
    return -1;
  }
  if ( a.date > b.date ){
    return 1;
  }
  return 0;
}

var ctx = document.getElementById('myChart').getContext('2d');
  
fetch("https://2tp0wsvdr2.execute-api.ap-southeast-2.amazonaws.com/live/cumulativedata", {
  "headers": {},
  "referrer": "",
  "referrerPolicy": "no-referrer-when-downgrade",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
})
.then((resp) => resp.json())
.then(function displayChart(chartData) {
	
	const colors = {
	  green: {
	    fill: '#e0eadf',
	    stroke: '#5eb84d',
	  },
	  lightBlue: {
	    stroke: '#6fccdd',
	  },
	  darkBlue: {
	    fill: '#92bed2',
	    stroke: '#3282bf',
	  },
	  purple: {
	    fill: '#8fa8c8',
	    stroke: '#75539e',
	  },
	};
	
	const cases = [];
	const deaths = [];
	const recovered = [];
	const date = [];
	
	var records = chartData['records'];
	
	records.sort( compare );
	
	for(var i=0; i<records.length; i++){
	  date.push(records[i]['date']);
	  deaths.push(records[i]['deaths']);
	  recovered.push(records[i]['recovered']);
	  cases.push(records[i]['cases']);
	}
	
	const myChart = new Chart(ctx, {
	  type: 'line',
	  data: {
	 
	    labels: date,
	    datasets: [{
	      label: "Recovered",
	      fill: true,
	      backgroundColor: colors.purple.fill,
	      pointBackgroundColor: colors.purple.stroke,
	      borderColor: colors.purple.stroke,
	      pointHighlightStroke: colors.purple.stroke,
	      borderCapStyle: 'butt',
	      data: recovered,
	
	    }, {
	      label: "Deaths",
	      fill: true,
	      backgroundColor: colors.darkBlue.fill,
	      pointBackgroundColor: colors.darkBlue.stroke,
	      borderColor: colors.darkBlue.stroke,
	      pointHighlightStroke: colors.darkBlue.stroke,
	      borderCapStyle: 'butt',
	      data: deaths,
	    }, {
	      label: "Cases",
	      fill: true,
	      backgroundColor: colors.green.fill,
	      pointBackgroundColor: colors.lightBlue.stroke,
	      borderColor: colors.lightBlue.stroke,
	      pointHighlightStroke: colors.lightBlue.stroke,
	      borderCapStyle: 'butt',
	      data: cases,
	    }]
	  },
	  options: {
	    responsive: false,
	    // Can't just just `stacked: true` like the docs say
	    scales: {
	      yAxes: [{
	        stacked: true,
	      }]
	    },
	    animation: {
	      duration: 750,
	    },
	    title: {
            display: true,
            text: 'USA COVID-19 Data (Cumulative)'
        }
	  }
	});
});