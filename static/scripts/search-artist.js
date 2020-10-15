function search_artist() {
  // Declare variables
  var input, filter, i, txtValue;
  input = document.getElementById('search_artist');
  filter = input.value.toUpperCase();

  var elements = document.getElementsByClassName("btn btn-default");

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < elements.length; i++) {
    txtValue = elements[i].textContent;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      elements[i].style.display = "";
    } else {
      elements[i].style.display = "none";
    }
  }
}