#! /bin/zsh

cd $1
main_file="$1/Reddit-sigs"
final_file="$1/result"
touch "result"
touch "files_list"

ls -1 | grep "signatures" >> files_list
#echo $files
files_list="$1/files_list"

while read line; do
  echo "$line"
  echo "--- Comparing with $line ---" >> $final_file
  comm -12 "$1/$line" $main_file >> $final_file
  echo -e "\n" >> $final_file ## Adding a newline
  echo "DONE"
done < "$files_list"

rm $files_list

