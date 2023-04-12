#!/bin/zsh

# Script to install pods for all the given versions
# Argument 1 = Name of Library
# Argument 2 = Path of the pods folder

if [ $# -eq 0 ];
then
    echo "--- No command arguments passed ---"
    echo "-> To use the script:"
    echo "       -> Arg[1] = Name of the Library;"
    echo "       -> Arg[2] = Path of the pods directory"

    echo "-> Requirements of the script:"
    echo "      -> signature.py and main.sh should be present in the same directory"
    exit
fi

echo "The script creates a new folder in the current directory with the output files"
current_dir=$(pwd)
signature_file_path=$current_dir/signature.py

library_name=$1
#versions=(0.10.0 0.10.1 0.5.1 0.7.0 0.9.0 0.9.1 0.9.2 1.0.1 1.0 1.0RC1 1.0RC2 1.0RC3 1.1.0 1.1.1 1.2.0 1.2.1 1.3.0 1.3.1 1.3.2 1.3.3 1.3.4 2.0.0-RC1 2.0.0-RC2 2.0.0-RC3 2.0.0 2.0.1 2.0.2 2.0.3 2.1.0 2.2.0 2.2.1 2.2.2 2.2.3 2.2.4 2.3.0 2.3.1 2.4.0 2.4.1 2.5.0 2.5.1 2.5.2 2.5.3 2.5.4 2.6.0 2.6.1 2.6.2 2.6.3 2.7.0 3.0.0-beta.1 3.0.0-beta.2 3.0.0-beta.3 3.0.0 3.0.1 3.0.2 3.0.3 3.0.4 3.1.0 3.2.0 3.2.1 4.0.0 4.0.1)
#versions=(0.1.2 0.1.3 0.1.4 0.2.1 0.2.2 0.2.3 0.3.0 0.4.0) 
versions=(0.4.0)

rm -rf output
mkdir output
op_dir="$current_dir/output"

for (( i=${#versions[@]}; i>0; i-- ));
do
    cp -rf $2 $current_dir
    cd $current_dir/pods
    version_number=${versions[$i]}
    new_file="""platform :ios, '11.0'
    target 'pods' do
      use_frameworks!
      pod '$library_name', '$version_number'
    end
    """

    touch Podfile
    echo $new_file > Podfile
    pod install
    
    echo "-> Pod installation done"
    
    ## Clean and Build the workspace
    xcodebuild clean -workspace pods.xcworkspace -scheme pods 2>/dev/null
    xcodebuild -workspace pods.xcworkspace -scheme $1 > /dev/null 2>&1
    
    build_return_val=$(echo $?)
    if [ $build_return_val -eq 0 ]; then
        echo "** BUILD SUCCEEDED **"
    else
        echo "** BUILD FAILED **"
        sleep 3
        mkdir $current_dir/output
        echo $version_number >>  $op_dir/fails 
        rm -rf $current_dir/pods
        rm -rf $HOME/Library/Developer/Xcode/DerivedData/pods*
        continue
    fi
    
    find $HOME/Library/Developer/Xcode/DerivedData/ -type f -name $library_name >> temporary
    read -r file < temporary
    echo "Library Path: $file"

    ## Invoking signature script
    cd $op_dir
    cp $file $op_dir

    # python3 $signature_file_path $library_name $version_number $wrk_dir
    echo "--- Signatures Created ---"
    
    #rm "$op_dir/$library_name"
    rm -rf $current_dir/pods
    rm -rf $HOME/Library/Developer/Xcode/DerivedData/pods*
    
    echo "--- Complete Process Done for $library_name-$version_number"
    sleep 3
done

