function get_tiny_url() {
    document.getElementById('response_section').style.display = 'none'
    document.getElementById('on_success').style.display = 'none'
    document.getElementById('on_failure').style.display = 'none'
    base_url = document.getElementById("base_url").value;
    fetch('post_new_url', {
            method: "POST",
            body: JSON.stringify({ 'base_url': base_url }),
            headers: new Headers({
                "content-type": "application/json"
            })
        }).then(function(response) {
            if (response.status !== 200) {
                data = { 'error': `Looks like there was a problem. Status code: ${response.status}` }
                handle_response(data)
                return
            }
            response.json().then(function(data) {
                handle_response(data)
                return
            });
        })
        .catch(function(error) {
            data = { 'error': `Looks like there was a problem. ${error}` }
            handle_response(data)
        });

}

function handle_response(data) {
    document.getElementById('response_section').style.display = ''
    if (data['success'] == true) {
        tiny_url = data['tiny_url']
        document.getElementById('on_success').style.display = ''
        document.getElementById('tiny_url_output').href = tiny_url
        document.getElementById('tiny_url_output').innerHTML = tiny_url
    } else {
        document.getElementById('on_failure').style.display = ''
        document.getElementById('error_output').innerHTML = data['error']
    }
}