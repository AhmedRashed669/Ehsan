firebase.initializeApp({
  apiKey: "AIzaSyAcbwVFge8wF_lvzP6cfiVsvZIy9AiZNEI",
  authDomain: "ehsan-d211b.firebaseapp.com",
  projectId: "ehsan-d211b",
  storageBucket: "ehsan-d211b.appspot.com",
  messagingSenderId: "221541812002",
  appId: "1:221541812002:web:1c9b656bce39778220877b",
});

const messaging = firebase.messaging();
navigator.serviceWorker.ready
  .then((registration) => {
    console.log("Service Worker Ready: ", registration);
    messaging.onMessage((payload) => {
      console.log("Message received. ", payload);
      const {
        notificationTitle = payload.notification.title,
        notificationOptions = {
          body: payload.notification.body,
          icon: payload.notification.image,
        },
      } = payload.notification;
      self.addEventListener("notificationclick", function (event) {
        event.notification.close();
        clients.openWindow(payload.url);
      });

      return registration.showNotification(
        notificationTitle,
        notificationOptions
      );
    });

    // You can use the registration object here.
  })
  .catch((error) => {
    console.error(
      "An error occurred while getting the service worker registration: ",
      error
    );
  });
