document.addEventListener("DOMContentLoaded", function () {
    const formInputs = document.querySelectorAll(".form-input");
  
    formInputs.forEach((input) => {
      // Função para verificar se o campo está preenchido
      const checkValue = () => {
        if (input.value) {
          input.classList.add("filled");
        } else {
          input.classList.remove("filled");
        }
      };
  
      // Verifica valor ao carregar a página (para preenchimento automático)
      checkValue();
  
      // Verifica valor ao foco e desfoco do campo
      input.addEventListener("input", checkValue);
      input.addEventListener("focus", checkValue);
      input.addEventListener("blur", checkValue);
    });
  });
  