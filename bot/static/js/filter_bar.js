/* JS used to handle the filter bar options */

(function () {
  const SELECTORS = {
    statusItem: '[aria-labelledby="statusDropdown"] .dropdown-item',
    statusInput: "statusInput",
    monthItem: '[aria-labelledby="monthDropdown"] .dropdown-item',
    monthInput: "monthInput",
    yearItem: '[aria-labelledby="yearDropdown"] .dropdown-item',
    yearInput: "yearInput",
  };

  document.querySelectorAll(SELECTORS.statusItem).forEach((item) => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      document.getElementById(SELECTORS.statusInput).value = item.dataset.value;
      item.closest("form").submit();
    });
  });

  document.querySelectorAll(SELECTORS.monthItem).forEach((item) => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      document.getElementById(SELECTORS.monthInput).value = item.dataset.value;
      item.closest("form").submit();
    });
  });

  document.querySelectorAll(SELECTORS.yearItem).forEach((item) => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      document.getElementById(SELECTORS.yearInput).value = item.dataset.value;
      item.closest("form").submit();
    });
  });
})();
