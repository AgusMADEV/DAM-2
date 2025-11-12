/**
 * Componente DatePicker (selector de fechas)
 * 
 * Uso:
 * <div class="je-datepicker"
 *      data-label="Fecha de entrega"
 *      data-format="dd/mm/yyyy"
 *      data-min="2025-01-01"
 *      data-max="2025-12-31">
 * </div>
 */
class JEDatePicker extends JEComponent {
  init() {
    this.labelText = this.root.dataset.label || "Fecha";
    this.format = this.root.dataset.format || "dd/mm/yyyy";
    this.minDate = this.root.dataset.min || null;
    this.maxDate = this.root.dataset.max || null;
    this.required = this.root.dataset.required === "true";
    
    this.selectedDate = null;
    this.currentMonth = new Date();
    this.isOpen = false;
    
    this.build();
    this.attachEvents();
  }

  build() {
    this.root.classList.add("je-field", "je-datepicker-wrapper");
    
    // Label
    const label = document.createElement("label");
    label.className = "je-label";
    label.textContent = this.labelText + (this.required ? " *" : "");
    
    // Input contenedor
    this.inputContainer = document.createElement("div");
    this.inputContainer.className = "je-datepicker-input";
    
    this.display = document.createElement("input");
    this.display.type = "text";
    this.display.className = "je-input";
    this.display.placeholder = this.format;
    this.display.readOnly = true;
    
    this.calendarIcon = document.createElement("span");
    this.calendarIcon.className = "je-datepicker-icon";
    this.calendarIcon.innerHTML = "📅";
    
    this.inputContainer.appendChild(this.display);
    this.inputContainer.appendChild(this.calendarIcon);
    
    // Calendario desplegable
    this.calendar = document.createElement("div");
    this.calendar.className = "je-datepicker-calendar";
    this.calendar.style.display = "none";
    
    // Ensamblar
    this.root.innerHTML = "";
    this.root.appendChild(label);
    this.root.appendChild(this.inputContainer);
    this.root.appendChild(this.calendar);
    
    this.renderCalendar();
  }

  attachEvents() {
    // Abrir/cerrar calendario
    this.inputContainer.addEventListener("click", () => {
      this.toggleCalendar();
    });
    
    // Cerrar al hacer click fuera
    document.addEventListener("click", (e) => {
      if (!this.root.contains(e.target) && this.isOpen) {
        this.closeCalendar();
      }
    });
  }

  toggleCalendar() {
    if (this.isOpen) {
      this.closeCalendar();
    } else {
      this.openCalendar();
    }
  }

  openCalendar() {
    this.calendar.style.display = "block";
    this.isOpen = true;
    this.renderCalendar();
  }

  closeCalendar() {
    this.calendar.style.display = "none";
    this.isOpen = false;
  }

  renderCalendar() {
    const year = this.currentMonth.getFullYear();
    const month = this.currentMonth.getMonth();
    
    // Header del calendario
    const header = document.createElement("div");
    header.className = "je-datepicker-header";
    
    const prevBtn = document.createElement("button");
    prevBtn.type = "button";
    prevBtn.className = "je-datepicker-nav";
    prevBtn.innerHTML = "‹";
    prevBtn.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      this.currentMonth = new Date(year, month - 1, 1);
      this.renderCalendar();
    });
    
    const monthYear = document.createElement("span");
    monthYear.className = "je-datepicker-month";
    monthYear.textContent = this.getMonthName(month) + " " + year;
    
    const nextBtn = document.createElement("button");
    nextBtn.type = "button";
    nextBtn.className = "je-datepicker-nav";
    nextBtn.innerHTML = "›";
    nextBtn.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      this.currentMonth = new Date(year, month + 1, 1);
      this.renderCalendar();
    });
    
    header.appendChild(prevBtn);
    header.appendChild(monthYear);
    header.appendChild(nextBtn);
    
    // Días de la semana
    const weekdays = document.createElement("div");
    weekdays.className = "je-datepicker-weekdays";
    ["Lu", "Ma", "Mi", "Ju", "Vi", "Sá", "Do"].forEach(day => {
      const dayEl = document.createElement("div");
      dayEl.textContent = day;
      weekdays.appendChild(dayEl);
    });
    
    // Días del mes
    const days = document.createElement("div");
    days.className = "je-datepicker-days";
    
    // Primer día del mes
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    
    // Ajustar para que lunes sea 0
    const startDay = firstDay === 0 ? 6 : firstDay - 1;
    
    // Días vacíos al inicio
    for (let i = 0; i < startDay; i++) {
      const emptyDay = document.createElement("div");
      emptyDay.className = "je-datepicker-day je-datepicker-day-empty";
      days.appendChild(emptyDay);
    }
    
    // Días del mes
    for (let day = 1; day <= daysInMonth; day++) {
      const dayEl = document.createElement("div");
      dayEl.className = "je-datepicker-day";
      dayEl.textContent = day;
      
      const currentDate = new Date(year, month, day);
      
      // Verificar si es el día seleccionado
      if (this.selectedDate && this.isSameDay(currentDate, this.selectedDate)) {
        dayEl.classList.add("je-datepicker-day-selected");
      }
      
      // Verificar si es hoy
      if (this.isSameDay(currentDate, new Date())) {
        dayEl.classList.add("je-datepicker-day-today");
      }
      
      // Verificar si está fuera del rango
      if (this.isDateDisabled(currentDate)) {
        dayEl.classList.add("je-datepicker-day-disabled");
      } else {
        dayEl.addEventListener("click", (e) => {
          e.preventDefault();
          e.stopPropagation();
          this.selectDate(currentDate);
        });
      }
      
      days.appendChild(dayEl);
    }
    
    // Limpiar y renderizar (pero mantener display)
    const currentDisplay = this.calendar.style.display;
    this.calendar.innerHTML = "";
    this.calendar.appendChild(header);
    this.calendar.appendChild(weekdays);
    this.calendar.appendChild(days);
    this.calendar.style.display = currentDisplay;
  }

  selectDate(date) {
    this.selectedDate = date;
    this.display.value = this.formatDate(date);
    this.closeCalendar();
    
    this.root.dispatchEvent(new CustomEvent("je:date:change", {
      detail: { date: date, formatted: this.formatDate(date) },
      bubbles: true
    }));
  }

  formatDate(date) {
    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const year = date.getFullYear();
    
    return this.format
      .replace("dd", day)
      .replace("mm", month)
      .replace("yyyy", year);
  }

  isSameDay(date1, date2) {
    return date1.getDate() === date2.getDate() &&
           date1.getMonth() === date2.getMonth() &&
           date1.getFullYear() === date2.getFullYear();
  }

  isDateDisabled(date) {
    if (this.minDate) {
      const min = new Date(this.minDate);
      if (date < min) return true;
    }
    if (this.maxDate) {
      const max = new Date(this.maxDate);
      if (date > max) return true;
    }
    return false;
  }

  getMonthName(month) {
    const months = [
      "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
      "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ];
    return months[month];
  }

  getValue() {
    return this.selectedDate;
  }

  setValue(date) {
    if (date instanceof Date) {
      this.selectDate(date);
    } else if (typeof date === "string") {
      this.selectDate(new Date(date));
    }
  }
}

JERegistry.register(".je-datepicker", JEDatePicker);
