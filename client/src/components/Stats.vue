<template>
  <section class="center-screen">
    <h1>Stats Page</h1>
    <div class="alert alert-success" id="url_registrations_count"></div>
<!--    <section class="row">-->
<!--      <canvas class="col" id="time_stats" width="700" height="300"></canvas>-->
<!--    </section>-->
    <chart :chartdata="datacollection" v-if="dataLoaded"></chart>

  </section>
</template>

<script>
import Chart from "./Chart.vue";

export default {
  components: {
    Chart
  },
  data () {
    return {
      datacollection: null,
      dataLoaded: false,
    }
  },
  methods: {
    get_data() {
      fetch('http://localhost:5000/stats', {
        method: 'GET',
        headers: new Headers({
          'content-type': 'application/json',
        }),
      }).then((response) => {
        if (response.status !== 200) {
          const data = { error: `Looks like there was a problem. Status code: ${response.status}` };
          return data;
        }
        response.json().then((data) => {
          this.draw_number(data.stats_data.url_redirection_registrations_count);
          // this.draw_bar(data.stats_data.time_stats, 'time_stats');
          this.datacollection = data.stats_data.time_stats;
          this.dataLoaded = true;
        });
      })
        .catch((error) => {
          const data = { error: `Looks like there was a problem. ${error}` };
          return data;
        });
    },
    draw_bar(data, elementId) {
      const ctx = document.getElementById(elementId);
      new Bar(ctx, {
        type: 'bar',
        data: {
          labels: data.labels,
          datasets: data.data_objects,
        },
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
      });
    },
    draw_number(data) {
      const element = document.getElementById('url_registrations_count');
      element.innerHTML = `<strong>${data}</strong>   Redirections in the DB`;
    },
  },
  created() {
    this.get_data();
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
 @import '../assets/css/style.css';
</style>
