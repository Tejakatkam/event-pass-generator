// Initialize EmailJS with your Public Key
(function() {
  emailjs.init("LW8AvJdD_7yUt0D9M"); 
})();

document.getElementById("gatePassForm").addEventListener("submit", async function(e) {
  e.preventDefault();

  let name = document.getElementById("name").value;
  let id = document.getElementById("id").value;
  let email = document.getElementById("email").value;

  // Create formatted text for QR code
  let qrData = `EVENT PASS DETAILS
------------------------
Name: ${name}
ID: ${id}
Email: ${email}
------------------------
Generated: ${new Date().toLocaleString()}
Valid for: Single Entry
Status: APPROVED ✓`;

  // Clear previous QR
  document.getElementById("qrcode").innerHTML = "";

  // Generate QR Code
  let canvas = document.createElement("canvas");
  await QRCode.toCanvas(canvas, qrData, { width: 200, margin: 2 });
  document.getElementById("qrcode").appendChild(canvas);

  // Convert QR Code to Base64 Image
  let qrImage = canvas.toDataURL("image/png");

  // Send email via EmailJS
  emailjs.send("service_4noajtf", "template_eh5mdow", {
    name: name,
    id: id,
    email: email,
    qr_code: qrImage
  })
  .then(function(response) {
    console.log("SUCCESS!", response.status, response.text);
    console.log("Email sent to:", email);
    alert("✅ Gate Pass sent successfully to " + email);
  }, function(error) {
    console.error("FAILED...", error);
    console.log("Data being sent:", { email, name, id });
    alert("❌ Failed to send Gate Pass. Error: " + error.text);
  });
});
