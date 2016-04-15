function run {
	echo
	echo "####################   ./mn $1 --help   ####################"
	
	./mn $1 --help
}

run
run create
run edit-ignores
run status
run update
