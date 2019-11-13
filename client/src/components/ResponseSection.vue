<template>
            <!-- response section -->
        <section id="response_section">
          <strong>{{ message.prefix }}</strong>  {{ message.postfix }}
        </section>
</template>

<script>

export default {
  props: ['message'],
};

</script>
