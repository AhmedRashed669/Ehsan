// const sendBtn = document.getElementById('sign');

// const ax = axios.create({
//     baseURL : 'http://127.0.0.1:8000/',
//     headers : {
//         'Authorization' : 'Token 5bd998309ea96695b03a47d9e1e35dc86ea0f675'
//     }
// });


const sendData = () => {
  // Get the username and password from the form
  const usernameField = document.querySelector('#id_username');
  const passwordField = document.querySelector('#id_password');

  axios.post('http://127.0.0.1:8000/accounts/login/', {     
      username: usernameField.value,
      password: passwordField.value,
  }, {
    withCredentials: true,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',  // Change the Content-Type
      'X-CSRFTOKEN': CSRF_TOKEN,
    },
  })
  .then(response => {
    console.log("Received response: ", response.data);  // Print received response
    if (response.data['message'] === true ) {
      window.location.replace("http://www.w3schools.com");
    } else {
      // Set the fields to null
      usernameField.value = '';
      passwordField.value = '';
      alert('Wrong Credentials')

    }
  });
};



// sendBtn.addEventListener('click',sendData);
// // console.log(CSRF_TOKEN);
// axios.post('http://127.0.0.1:8000/accounts/test/',{
//     shit : 'shit'
// }).then(response =>{
//     console.log(response.data.shit);
// });