<template>
  <div id="app">
    <div>
      <b-navbar toggleable="lg" type="light" variant="light">
        <b-navbar-brand href="/">Home</b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item href="/stats">Statistics</b-nav-item>
          </b-navbar-nav>

        </b-collapse>
      </b-navbar>
    </div>

    <router-view/>
  </div>
</template>

<style>

</style>
