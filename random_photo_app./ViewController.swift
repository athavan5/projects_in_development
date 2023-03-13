//
//  ViewController.swift
//  RandomPhoto
//
//  Created by Athavan Gananathan on 2023-03-11.
//

import UIKit

class ViewController: UIViewController {

    private let imageView: UIImageView = {
        let imageView = UIImageView()
        imageView.contentMode = .scaleAspectFill //ensures image maintains aspect ratio
        imageView.backgroundColor = .red
        return imageView
    }()
    
    //represents button to click on
    private let button: UIButton = {
        let button = UIButton()
        button.backgroundColor = .white
        button.setTitle("SELECT NEW PHOTO", for: .normal)
        button.setTitleColor(.green, for: .normal)
        return button
    }()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .systemBlue //changes background colour to blue
        view.addSubview(imageView) //allows image to be added on screen
        
        imageView.frame = CGRect(x: 0, y: 0, width: 300, height: 300)
        imageView.center = view.center
        
        view.addSubview(button) //allows button to be added on screen
        
        getRandomPhoto()
        button.addTarget(self, action: #selector(didTapButton), for: .touchUpInside)
    }
    
    override func viewDidLayoutSubviews() {
        super.viewDidLayoutSubviews()
        
        button.frame = CGRect(x: 30, y: view.frame.size.height-150-view.safeAreaInsets.bottom, width: view.frame.size.width-60, height: 55)
        
    }
    
    @objc func didTapButton(){
        getRandomPhoto()
    }
    
    func getRandomPhoto(){
        let urlString =
            "https://source.unsplash.com/random/600x600"
        let url = URL(string: urlString)!
        guard let data = try? Data(contentsOf: url) else{
            return
        }
        
        imageView.image = UIImage(data: data)
    }
}

