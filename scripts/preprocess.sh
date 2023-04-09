#! /bin/bash

if [ $# -eq 0 ];
then
	echo "--- Script needs command line arguments ---"
	echo "-> Usage: ./script.sh [Absolute path of the directory with only IPA files]"
	exit
fi

echo "-> This is an automated script to get the list of libraries used by an ipa file(s)"

initial_path=$(pwd)
mkdir lib_data
cd $1

files=$(ls -1)

## loop to extract IPA files
for var in $files
do
	filename_length=${#var}
	new_var=${var:0:($filename_length-4)}		# removing .ipa from filename
	payload_dir="$new_var.dir"
	mkdir $payload_dir
	cd $payload_dir
	ext=$(unzip ../$var > /dev/null)					# supressing the command output
	cd ..
done

# loop to find the Mach-O file and implement otool on the same
IFS=$'\n'
dirs=$(ls -1 | grep ".dir")
for varr in $dirs 
do
	cd "$1"
	cd "$varr"
	flag=$(ls | grep "Payload")
	flag_check="Payload"
	ipa_name=${varr:0:(${#varr}-4)}
	if [[ "$flag" = "$flag_check" ]]
	then
		cd $flag
	else
		cd "$initial_path/lib_data"
		$(touch -c fails)
		echo ">> *ERROR*: No Payload for '$varr' <<"
		$(echo $ipa_name >> "$initial_path/lib_data/fails")
		continue
	fi
	
	app_name=$(ls | grep *.app)
	cd $app_name
	app_name_len=${#app_name}
	if [[ "$app_name" =~ ( |\') ]]  ## condition if file name has spaces
	then
		exec=""
		exec+=${app_name:0:($app_name_len-4)}
		exec+=""
	else
		exec=${app_name:0:($app_name_len-4)}
	fi

	echo ">>> Operating on the Application - <$ipa_name>"
	arch=$(lipo -archs $exec)
	len=${#arch}
	
	if [[ "$len" -gt 5 ]] ## condition if the Mach-O file supports multiple architectures
	then
		libs=$(otool -L $exec -arch arm64 | grep '@' | grep '.framework') # considering only third-party libraries/frameworks
	else
		libs=$(otool -L $exec | grep '@' | grep '.framework')
	fi
	echo "-> Otool implementation done!!"

	cd "$initial_path/lib_data"
	for string in $libs
	do 
		# filtering the library name from the output of otool
		IFS=' '
		arr=()
		read -ra arr <<< "$string"
		for val in "${arr[@]}";
		do
			IFS='/'
			arr2=()
			read -ra arr2 <<< "$val"
			final=""
			for val2 in "${arr2[@]}";
			do
				final=$val2
			done
			$(echo $final >> ./$ipa_name)	
			break
		done
		IFS=''
	done
	echo "-> $lib_file_name libraries stored"
	sleep 1
done
