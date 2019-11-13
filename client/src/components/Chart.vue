<script>
import { Bar } from 'vue-chartjs';

export default {
  extends: Bar,
  data() {
    return {
      options: {
        title: {
          display: true,
          text: 'Time based stats',
        },
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true,
            },
          }],
        },
      },
    };
  },
  props: ['chartdata'],
  mounted() {
    this.renderChart(this.chartdata, this.options);
  },
};
</script>

<style>
</style>
