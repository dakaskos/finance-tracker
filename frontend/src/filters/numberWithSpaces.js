export function numberWithSpaces(value) {
  if (value == null) return ''; // Check for null or undefined

  // Convert the number to a string
  value = value.toString();

  // Split the integer and decimal parts
  const parts = value.split('.');

  // Format the integer part with spaces
  parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ' ');

  // Join the integer and decimal parts back together
  return parts.join('.');
}
