/* JS to open the modal using the DJANGO views.py */

(function () {
  const SELECTORS = {
    modal: "historyDetailsModal",
  };

  const modal = new bootstrap.Modal(document.getElementById(SELECTORS.modal));
  modal.show();
})();
