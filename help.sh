function run {
	echo
	echo "####################   ./mn $1 --help   ####################"
	
	./mn $1 --help
}

run
run edit-ignores
run init
run status
run add
run remove
