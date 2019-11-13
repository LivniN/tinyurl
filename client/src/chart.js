import {Chart} from 'vue-chartjs'

export default {
  extends: Chart,
  props: ['chartData', 'options'],
  data() {
    return {
      type: 'bar',
      options: {
        title: {
          display: true,
          text: 'Time based stats'
        },
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        }
      }
    }
  },
  mounted() {
    this.renderChart(this.chartdata, this.options)
  }

}
