import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../components/Home.vue';
import Stats from '../components/Stats.vue';

Vue.use(VueRouter);

const routes = [{
  path: '/',
  name: 'home',
  component: Home,
},
{
  path: '/stats',
  name: 'stats',
  component: Stats,
},

];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
