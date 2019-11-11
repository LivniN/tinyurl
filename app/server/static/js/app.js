function get_short_url() {
    document.getElementById('response_section').style.display = 'none'
    document.getElementById('on_success').style.display = 'none'
    document.getElementById('on_failure').style.display = 'none'
    long_url = document.getElementById("long_url").value;
    fetch('post_new_url', {
            method: "POST",
            body: JSON.stringify({ 'long_url': long_url }),
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
        short_url = data['short_url']
        document.getElementById('on_success').style.display = ''
        document.getElementById('short_url_output').href = short_url
        document.getElementById('short_url_output').innerHTML = short_url
    } else {
        document.getElementById('on_failure').style.display = ''
        document.getElementById('error_output').innerHTML = data['error']
    }
}