// Example 8: Nested loops and conditions
var i;
var j;

for (i = 1; i <= 3; i = i + 1) {
    for (j = 1; j <= 3; j = j + 1) {
        if (i == j) {
            print i;
        }
    }
}

// Results: 1, 2, 3
