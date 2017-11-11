function OkayNav(target, rawopts) {
	// setup instance
	var self = this;

	// setup options
	var opts = Object(rawopts);

	// get target
	self.target = findOrElement(target);

	self.target.setAttribute('data-okay-target', '');

	// get measure element
	self.measure = findOrElement(opts.measure) || target.parentNode;

	// get navigation items
	self.items = typeof opts.items === 'string' ? document.querySelectorAll(opts.items) : opts.items;

	self.items = self.items || target.querySelectorAll('li');

	self.items = Array.prototype.slice.call(self.items);

	self.items.forEach(function (item) {
		item.setAttribute('data-okay-item', '');
	});

	// get toggle element
	self.toggle = findOrElement(opts.toggle) || document.createElement('button');

	self.toggle.setAttribute('aria-expanded', 'false');

	self.toggle.setAttribute('aria-hidden', '');

	self.toggle.setAttribute('data-okay-toggle', '');

	self.toggle.addEventListener('click', function () {
		self.toggleOverflow();
	});

	if (!self.toggle.parentNode) {
		self.toggle.innerHTML = `
			<nav class="navbar navbar-light">
				<button class="navbar-toggler" type="button" aria-label="Toggle navigation">
					<span class="navbar-toggler-icon"></span>
				</button>
			</nav>
		`

		self.target.appendChild(self.toggle);
	}

	// get overflow element
	self.overflow = findOrElement(opts.overflow) || document.createElement('ul');

	// configure overflow element
	self.overflow.setAttribute('aria-hidden', '');

	self.overflow.setAttribute('data-okay-overflow', '');

	if (!self.overflow.parentNode) {
		self.target.appendChild(self.overflow);
	}

	// setup overflow items
	self.overflowItems = [];

	// setup padding space
	self.padding = opts.padding || 0;

	// call resize event on window resizes
	window.addEventListener('resize', function () {
		self.recalculate();
	});

	// when the target loses focus
	self.target.addEventListener('blur', function (event) {
		// wait a moment to see what receives focus
		setTimeout(function () {
			// conditionally close overflow if focus has left the navigation
			if (!self.target.contains(document.activeElement)) {
				self.hideOverflow();
			}
		}, 16);
	}, true);
	console.log(self)
	// call resize event
	self.recalculate();
};

OkayNav.prototype.recalculate = function recalculate() {
	var self = this;

	// conditionally run xuc on animation frame changes
	if (!self._currentAnimationFrame) {
		self._currentAnimationFrame = requestAnimationFrame(function () {
			delete self._currentAnimationFrame;
		});

		// get the difference
		var width = getMeasureWidth(self);
		console.log("self.padding: ",self.padding)
		console.log("width: ",width)
		// if the difference is small
		if (width < self.padding) {
			console.log("it is small")
			var hasToggle = self.toggle.hasAttribute('aria-hidden');

			while (self.items.length && width < self.padding) {
				var lastChild = self.items.pop();
				console.log(lastChild)
				if (hasToggle) {
					self.toggle.removeAttribute('aria-hidden');

					fire(self, self.target, 'showtoggle');

					hasToggle = false;
				}

				self.overflowItems.unshift({
					node:   lastChild,
					parent: lastChild.parentNode,
					width:  getOuterWidth(lastChild)
				});

				self.overflow.appendChild(lastChild);

				fire(self, lastChild, 'hideitem');

				width += self.overflowItems[0].width;

				if (width > 0) {
					width = getMeasureWidth(self);
				}
			}
		} else {
			console.log("it is big")
			// if there are items to restore
			if (self.overflowItems.length) {
				// while there are hidden items and the difference is greater than the width of the most recent hidden item
				while (self.overflowItems.length && (width > self.overflowItems[0].width + self.padding)) {
					var lastItem = self.overflowItems.shift();

					lastItem.parent.appendChild(lastItem.node);

					self.items.push(lastItem.node);

					width -= lastItem.width;

					fire(self, lastItem.node, 'showitem');
				}

				if (!self.overflowItems.length) {
					self.toggle.setAttribute('aria-expanded', 'false');
					self.toggle.setAttribute('aria-hidden', '');

					fire(self, self.target, 'hidetoggle');

					if (!self.overflow.hasAttribute('aria-hidden')) {
						self.overflow.setAttribute('aria-hidden', '');

						fire(self, self.target, 'hideoverflow');
					}
				}
			}
		}
	}
};

OkayNav.prototype.showOverflow = function showOverflow() {
	var self = this;

	if (self.toggle.getAttribute('aria-expanded') === 'false') {
		self.toggle.setAttribute('aria-expanded', 'true');

		self.overflow.removeAttribute('aria-hidden', '');

		fire(self, self.target, 'showoverflow');
	}
};

OkayNav.prototype.hideOverflow = function hideOverflow() {
	var self = this;

	if (self.toggle.getAttribute('aria-expanded') === 'true') {
		self.toggle.setAttribute('aria-expanded', 'false');

		self.overflow.setAttribute('aria-hidden', '');

		fire(self, self.target, 'hideoverflow');
	}
};

OkayNav.prototype.toggleOverflow = function hideOverflow() {
	if (this.overflow.hasAttribute('aria-hidden')) {
		this.showOverflow();
	} else {
		this.hideOverflow();
	}
};

function findOrElement(option) {
	return typeof option === 'string' ? document.querySelector(option) : option;
}

function getMeasureWidth(self) {
	return getInnerWidth(self.measure) - Array.prototype.reduce.call(self.measure.children, function (initialValue, child) {
		return initialValue + getOuterWidth(child);
	}, 0);
}

// fire event
function fire(self, element, type) {
	var event = document.createEvent('Event');

	event.initEvent('okaynav:' + type, true, false);

	event.detail = self;

	element.dispatchEvent(event);
}

// get element inner width
function getInnerWidth(element) {
	var computedStyle = getComputedStyle(element);

	return element.getBoundingClientRect().width - parseFloat(computedStyle.paddingLeft) - parseFloat(computedStyle.paddingRight);
}

// get element outer width
function getOuterWidth(element) {
	var computedStyle = getComputedStyle(element);

	return element.getBoundingClientRect().width + parseFloat(computedStyle.marginLeft) + parseFloat(computedStyle.marginRight);
}
