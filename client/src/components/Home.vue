<template>
<section class="center-screen">
    <h1>Tiny Url Generator</h1>
  <div class=" border rounded border-white">
        <!-- Get tiny url form -->
        <form id="get_url_form" class="row justify-content-center" @submit="get_short_url">
            <div class="form-group col-xs-5 col-lg-6">
                <div> Enter long url: </div>
            </div>
            <div class="form-group col-xs-5 col-lg-10">
                <!-- type should be url-->
              <input type="url" id="long_url"  name="long_url" class="form-control"
                placeholder=" www.somethingverylong.com/1234.html " required autofocus>
            </div>
            <div class="form-group col-xs-5 col-lg-6">
                <button class="btn btn-success" type="submit">Create short URL</button>
            </div>
        </form>
  <response_section  :message=message :class="responseClass" v-if="showMessage" ></response_section>
  </div>
</section>
</template>

<script>
import ResponseSection from './ResponseSection.vue';

export default {
  data() {
    return {
      showMessage: false,
      message: {
        prefix: '',
        postfix: '',
      },
      responseClass: '',
    };
  },
  components: {
    response_section: ResponseSection,
  },
  methods: {
    get_short_url(evnt) {
      evnt.preventDefault();
      const LongURL = document.getElementById('long_url').value;
      fetch('http://localhost:5000/post_new_url', {
        method: 'POST',
        body: JSON.stringify({ long_url: LongURL }),
        headers: new Headers({
          'content-type': 'application/json',
        }),
      }).then((response) => {
        if (response.status !== 200) {
          const data = { error: `Looks like there was a problem. Status code: ${response.status}` };
          this.handle_response(data);
          return;
        }
        response.json().then((data) => {
          this.handle_response(data);
        });
      })
        .catch(function (error) {
          const data = { error: `Looks like there was a problem. ${error}` };
          this.handle_response(data);
        });
    },
    handle_response(data) {
      if (data.success === true) {
        this.message.prefix = 'SUCCESS! short URL: ';
        this.message.postfix = `${data.short_url}`;
        this.responseClass = 'alert alert-success';
        this.showMessage = true;
      } else {
        this.message.prefix = 'ERROR!';
        this.message.postfix = `${data.error}`;
        this.responseClass = 'alert alert-danger';
        this.showMessage = true;
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
 @import '../assets/css/style.css';
</style>
