firebase.initializeApp({
  // Replace messagingSenderId with yours
  apiKey: "AIzaSyAcbwVFge8wF_lvzP6cfiVsvZIy9AiZNEI",
  authDomain: "ehsan-d211b.firebaseapp.com",
  projectId: "ehsan-d211b",
  storageBucket: "ehsan-d211b.appspot.com",
  messagingSenderId: "221541812002",
  appId: "1:221541812002:web:1c9b656bce39778220877b",
});

// Retrieve an instance of Firebase Messaging so that it can handle background
// messages.
const messaging = firebase.messaging();
// Listen for messages
// messaging.onMessage((payload) => {
//   console.log('Message received:', payload);

//   // Customize notification here
//   const notificationTitle = payload.notification.title;
//   const notificationOptions = {
//     body: payload.notification.body,
//     icon: payload.notification.icon,
//   };

//   // Display the notification
//   self.registration.showNotification(notificationTitle, notificationOptions);
// });

// messaging.onMessage((payload) => {
//   console.log('Message received. ', payload);
//   const {
//     notificationTitle = payload.notification.title,
//     notificationOptions = {
//       body: payload.notification.body,
//       icon: payload.notification.icon,
//     },
//   } = payload.notification;
//   navigator.serviceWorker.ready.then((registration) => {
//     registration.showNotification(title, options);
//   });
// });
messaging.onMessage((payload) => {
  console.log('Message received. ', payload);
  // ...
});