package main

import "fmt"

func main() {
	x := []int{1, 2, 3, 4, 5}

	fmt.Println(x[4])
	fmt.Println(x[4:5])
	fmt.Println(x[5:5])
}
