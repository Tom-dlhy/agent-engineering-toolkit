# Inputs, forms and selection controls

Consult only for forms, inputs, comboboxes, autocompletes, date/time pickers or grouped selections.

1. Map data ownership: form library or native/provider form state; controlled vs uncontrolled; no duplicate competing stores.
2. Match the installed provider API for field label, hint, error, invalid state, name, required/disabled/read-only and submission. Never assume that web Form, React Native FormControl and Angular Reactive Forms are interchangeable.
3. Check select/autocomplete/filter semantics: typed vs selected value, keyboard traversal, clear action, async options, empty and loading cases, multi-select tokens, max selections and virtualized options if needed.
4. Date/time controls need locale, calendar system, timezone, serialization and min/max validation decisions. The visible local date and stored instant may differ.
5. Verify accessible label and associated message, focus announcement, validation timing, touch targets, disabled controls and submit-on-enter. Test IME, browser autofill and mobile keyboards where relevant.

**Examples to research in provider docs:** shadcn Field/Select, React Aria ComboBox/DatePicker, Mantine useForm/DatePicker, MUI Autocomplete/DatePicker, Vuetify v-form, PrimeVue Form/Select, Angular MatFormField and Flutter Form/TextFormField.
