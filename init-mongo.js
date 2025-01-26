db = db.getSiblingDB("freelanceflow"); // Selektiraj ili kreiraj bazu "freelanceflow"

// Dodaj korisnika za aplikaciju
db.createUser({
  user: "st",
  pwd: "12345", // Promijeni na sigurnu lozinku
  roles: [{ role: "readWrite", db: "freelanceflow" }],
});

// Dodaj primjer podataka (opcionalno)
db.notifications.insertOne({
  user_id: 1,
  message: "Welcome to FreelanceFlow!",
  event_type: "welcome",
  is_read: false,
  created_at: new Date(),
});
