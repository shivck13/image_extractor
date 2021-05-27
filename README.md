# Structure
* module `extractor` contains a class called `GoogleImageExtractor`

# Requirements
* This module uses `selenium` webdriver module
* Chrome Web Driver binary should be placed at "./webdriver/chromedriver.exe" (or equivalent)

# Usage
<pre>
	<code>
		from extractor import GoogleImageExtractor

		bot = GoogleImageExtractor("Rakul", 10, "./Rakul Images", False)
		bot.apply_safesearch(False)
		bot.apply_search_filters(color="red")
		bot.run()
	</code>
</pre>

# Documentation
Description of *GoogleImageExtractor* class

## Class Methods

#### `constructor method`
The constructor method for the class

**Parameters**  
1. *required* `search_query` : str
	* The search term to search on Google Images
2. optional* `number_of_images` : int
* Number of images to fetch
	* default = `10`
3. *optional* `destination_folder` : str 
	* directory to save image files or url .log file
	* default = `current directory` [os.curdir]
4. *optional* `url_only` : bool
	* if set to `True` only urls will be saved not the actual image files
	* default = `False` 

#### `apply_safesearch()`
This method is used to turn safesearch on or off.

**Parameters**  
1. *optional* `safe` : bool
	* if set to `False` safesearch feature on Google Images will be disabled
	* default = `True`

#### `apply_search_filters()`
This method is used to set the search parameters

Note : parameter values of `str` type are `case-insensitive`

**Parameters**  
1. *optional* `size` : str 
	* size of images in search
	* possible values = `"any"` (default), `"large"`, `"medium"`, `"icon"`
2. *optional* `color` : str 
	* color of images 
	* possible values = `"any"` (default), `"black and white"`, `"transparent"`, `"red"`, `"orange"`, `"yellow"`, `"green"`, `"teal"`, `"blue"`, `"purple"`, `"pink"`, `"white"`, `"gray"`, `"black"`, `"brown"`
3. *optional* `type` : str 
	* type of image
	* possible values = `"any"` (default), `"clip art"`, `"line drawing"`, `"gif"`
4. *optional* time : str
	* time of images (how old)
	* possible values = `"any"` (default), `"past 24 hours"`, `"past week"` , `"past month"`, `"past year"`
5. license : str
	* license type of images
	* possible values = `"any"` (default), `"creative commons licenses"`, `"commercial & other licenses"`

#### `run()`
This method is used to execute the extractor. This saves images (in desired folder) or urls (in a .log file) as per choice

**parameters** - no parameters

______

## Class Variables

#### `webdriver_bin_path` : str
This is the binary path for chrome webdriver

#### `allowed_extensions` : list
This is `list` of allowed image extensions
default = ["png", "gif", "jpg", "jpeg", "webp", "bmp", "svg", "ico"]
