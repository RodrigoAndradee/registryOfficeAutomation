flatpickr("#datepicker", {
  dateFormat: "Y-m-d",
  locale: "pt",
  altInput: true,
  altFormat: "d/m/Y",
  allowInput: true,
});


document.querySelectorAll(".dropdown-item").forEach((item) => {
  item.addEventListener("click", function (e) {
    e.preventDefault();
    const selectedValue = this.getAttribute("data-value");
    const label = this.textContent.trim();

    document.getElementById("statusInput").value = selectedValue;
    document.getElementById("statusDropdown").textContent = label;
  });
});
