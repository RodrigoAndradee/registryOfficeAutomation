/* JS used to set the previous month on the modal */

(function () {
  const SELECTORS = {
    month: "monthSelect",
  };

  const now = new Date();
  const month = String(now.getMonth());

  const monthSelectElement = document.getElementById(SELECTORS.month);
  if (monthSelectElement) monthSelectElement.value = month;
})();
