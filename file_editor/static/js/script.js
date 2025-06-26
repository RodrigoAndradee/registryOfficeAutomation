tinymce.init({
  selector: "textarea#id_your_field", // Replace with your actual textarea ID
  plugins: "exportpdf", // Example plugin
  toolbar: "exportpdf",

  exportpdf_token_provider: () => {
    return fetch("http://localhost:3000/jwt", {
      // specify your token endpoint
      method: "POST",
      headers: { "Content-Type": "application/json" },
    }).then((response) => response.json());
  },

  content_style: "p { margin: 16px 0; }", // Apply custom margin to paragraphs
  // Add other TinyMCE configurations as needed
});
