#!/bin/zsh

library_name="AFNetworking"
versions=(0.10.0 0.10.1 0.5.1 0.7.0 0.9.0 0.9.1 0.9.2 1.0.1 1.0 1.0RC1 1.0RC2 1.0RC3 1.1.0 1.1.1 1.2.0 1.2.1 1.3.0 1.3.1 1.3.2 1.3.3 1.3.4 2.0.0-RC1 2.0.0-RC2 2.0.0-RC3 2.0.0 2.0.1 2.0.2 2.0.3 2.1.0 2.2.0 2.2.1 2.2.2 2.2.3 2.2.4 2.3.0 2.3.1 2.4.0 2.4.1 2.5.0 2.5.1 2.5.2 2.5.3 2.5.4 2.6.0 2.6.1 2.6.2 2.6.3 2.7.0 3.0.0-beta.1 3.0.0-beta.2 3.0.0-beta.3 3.0.0 3.0.1 3.0.2 3.0.3 3.0.4 3.1.0 3.2.0 3.2.1 4.0.0 4.0.1)

for (( i=${#versions[@]}; i>0; i-- ))
do
    cd $1
    version_number=${versions[$i]}
    new_file="platform :ios, '9.0'
    target 'pods' do
      use_frameworks!
      pod '$library_name', '$version_number'
    end
    "
    
    touch Podfile
    echo $new_file > Podfile
    pod install
    
    echo "--- Pod Installation Done ---"
    
    
    ## Clean and Build the workspace
    xcodebuild clean -workspace pods.xcworkspace -scheme pods 2>/dev/null
    xcodebuild build -workspace pods.xcworkspace -scheme pods > /dev/null 2>&1
    
    build_return_val=$(echo $?)
    if [ $build_return_val -eq 0 ]; then
        echo "** BUILD SUCCEEDED **"
    else
        echo "** BUILD FAILED **"
        sleep 3
        echo $version_number >> /Users/amfoss/Desktop/iOS-Project-Akshith/wrk_dir/fails
        rm -rf $1
        rm -rf /Users/amfoss/Library/Developer/Xcode/DerivedData/pods*
        cp -rf /Users/amfoss/Desktop/iOS-Project-Akshith/scripts/pods /Users/amfoss/Desktop/iOS-Project-Akshith
        continue
    fi
    
    
    
    find ~/Library/Developer/Xcode/DerivedData/ -type f -name $library_name >> temporary
    read -r file < temporary
    echo "Library Path: $file"

    ## Invoking signature script
    wrk_dir="/Users/amfoss/Desktop/iOS-Project-Akshith/wrk_dir"
    cp $file $wrk_dir
    python3 /Users/amfoss/Desktop/iOS-Project-Akshith/scripts/signature.py $library_name $version_number $wrk_dir

    echo "--- Signatures Created ---"
    
    rm "$wrk_dir/$library_name"
    rm -rf $1
    rm -rf /Users/amfoss/Library/Developer/Xcode/DerivedData/pods*
    cp -rf /Users/amfoss/Desktop/iOS-Project-Akshith/scripts/pods /Users/amfoss/Desktop/iOS-Project-Akshith
    
    echo "--- Complete Process Done for $library_name-$version_number"
    sleep 3
done
