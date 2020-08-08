// REFERENCE: https://github.com/samhita-alla/flask-chat-app-article

var socket = io.connect('https://' + document.domain + ':' + location.port);

socket.on( 'connect', function() { // reserved event name for handshake
  socket.emit('join_room', {
    user: user_id,
    group: group_id
  })

// interupt form submission and emit event instead
var form = $('#msg').on('submit', function(e) {
    e.preventDefault()
    //let user_name = $( 'input.username' ).val()
    let user_input = $( 'input.message' ).val()
    socket.emit( 'send_message', {
      user: user_id,
      username: user_name,
      group: group_id,
      message : user_input
    } )
    $( 'input.message' ).val( '' ).focus()
  } )
} )

// recieve event and update html
socket.on( 'recieved_message', function( data ) {
  console.log( data )
  $( 'h3' ).remove() // remove "no msgs" placeholder
  $( 'div.message_holder' ).append( '<div><b style="color: #000">'+data['username']+'</b> '+data['message']+'</div>' ) // add new msg
})
