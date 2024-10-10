const alert = document.getElementById('page-alert')
const closeBtn = document.getElementById('page-alert-btn-close')
if (alert !== null && closeBtn !== null) {
  const version = alert.getAttribute('data-page-alert-version') || 'unknown'
  const hideAlert = sessionStorage.getItem(`page-alert-${version}`) !== null
  if (hideAlert) {
    alert.classList.add('d-none')
  }

  closeBtn.addEventListener('click', () => {
    sessionStorage.setItem(`page-alert-${version}`, 'seen')
    alert.classList.add('d-none')
  })
}

;
// Adapted from https://github.com/gohugoio/hugo/blob/master/tpl/tplimpl/embedded/templates/google_analytics.html


;
function reveal () {
  const reveals = document.querySelectorAll('.reveal')

  for (let i = 0; i < reveals.length; i++) {
    const windowHeight = window.innerHeight
    const elementTop = reveals[i].getBoundingClientRect().top
    const elementVisible = 150

    if (elementTop < windowHeight - elementVisible) {
      reveals[i].classList.add('active')
      reveals[i].classList.remove('reveal')
    } else {
      reveals[i].classList.remove('active')
    }
  }
}

window.addEventListener('scroll', reveal)

;
/*
Source:
  - https://simplernerd.com/hugo-add-copy-to-clipboard-button/
*/

const svgCopy =
  '<svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" width="16" height="16" fill="currentColor" class="bi bi-clipboard" viewBox="0 0 16 16"><path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"/><path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"/></svg>'
const svgCheck =
  '<svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true"><path fill-rule="evenodd" fill="rgb(63, 185, 80)" d="M13.78 4.22a.75.75 0 010 1.06l-7.25 7.25a.75.75 0 01-1.06 0L2.22 9.28a.75.75 0 011.06-1.06L6 10.94l6.72-6.72a.75.75 0 011.06 0z"></path></svg>'

const addCopyButtons = (clipboard) => {
  // 1. Look for pre > code elements in the DOM
  document.querySelectorAll('pre > code').forEach((codeBlock) => {
    // 2. Create a button that will trigger a copy operation
    const button = document.createElement('button')
    button.className = 'clipboard-button'
    button.setAttribute('data-toast-target', 'toast-copied-code-message')
    button.setAttribute('aria-label', 'copy to clipboard')
    button.type = 'button'
    button.innerHTML = svgCopy
    button.addEventListener('click', () => {
      const text = codeBlock.innerText.split('\n').filter(Boolean).join('\n')
      clipboard.writeText(text).then(
        () => {
          button.blur()
          button.innerHTML = svgCheck
          setTimeout(() => (button.innerHTML = svgCopy), 2000)
        },
        // eslint-disable-next-line n/handle-callback-err
        (error) => (button.innerHTML = 'Error')
      )
    })
    // 3. Append the button directly before the pre tag
    const pre = codeBlock.parentNode
    pre.parentNode.insertBefore(button, pre)
  })
}

if (navigator && navigator.clipboard) {
  addCopyButtons(navigator.clipboard)
}

document.querySelectorAll('[data-clipboard]').forEach(trigger => {
  const text = trigger.getAttribute('data-clipboard')
  trigger.addEventListener('click', () => {
    navigator.clipboard.writeText(text)
  })
})

;
const url = new URL(window.location.href)
const menu = url.searchParams.get('menu')
const child = url.searchParams.get('child')
const menuItems = document.querySelectorAll('[data-nav="main"]')

if (menu !== null) {
  menuItems.forEach(element => {
    element.classList.remove('active')
  })

  const targetMainItems = document.querySelectorAll(`[data-nav-main="${menu}"]:not([data-nav-child])`)
  targetMainItems.forEach(element => {
    element.classList.add('active')
  })

  const targetChildItems = document.querySelectorAll(`[data-nav-main="${menu}"][data-nav-child="${child}"]`)
  targetChildItems.forEach(element => {
    element.classList.add('active')
  })
}

;
/*!
  * Bootstrap v5.3.3 (https://getbootstrap.com/)
  * Copyright 2011-2024 The Bootstrap Authors (https://github.com/twbs/bootstrap/graphs/contributors)
  * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
  */
(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
  typeof define === 'function' && define.amd ? define(factory) :
  (global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.bootstrap = factory());
})(this, (function () { 'use strict';

  /**
   * --------------------------------------------------------------------------
   * Bootstrap dom/data.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */

  /**
   * Constants
   */

  const elementMap = new Map();
  const Data = {
    set(element, key, instance) {
      if (!elementMap.has(element)) {
        elementMap.set(element, new Map());
      }
      const instanceMap = elementMap.get(element);

      // make it clear we only want one instance per element
      // can be removed later when multiple key/instances are fine to be used
      if (!instanceMap.has(key) && instanceMap.size !== 0) {
        // eslint-disable-next-line no-console
        console.error(`Bootstrap doesn't allow more than one instance per element. Bound instance: ${Array.from(instanceMap.keys())[0]}.`);
        return;
      }
      instanceMap.set(key, instance);
    },
    get(element, key) {
      if (elementMap.has(element)) {
        return elementMap.get(element).get(key) || null;
      }
      return null;
    },
    remove(element, key) {
      if (!elementMap.has(element)) {
        return;
      }
      const instanceMap = elementMap.get(element);
      instanceMap.delete(key);

      // free up element references if there are no instances left for an element
      if (instanceMap.size === 0) {
        elementMap.delete(element);
      }
    }
  };

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/index.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */

  const MAX_UID = 1000000;
  const MILLISECONDS_MULTIPLIER = 1000;
  const TRANSITION_END = 'transitionend';

  /**
   * Properly escape IDs selectors to handle weird IDs
   * @param {string} selector
   * @returns {string}
   */
  const parseSelector = selector => {
    if (selector && window.CSS && window.CSS.escape) {
      // document.querySelector needs escaping to handle IDs (html5+) containing for instance /
      selector = selector.replace(/#([^\s"#']+)/g, (match, id) => `#${CSS.escape(id)}`);
    }
    return selector;
  };

  // Shout-out Angus Croll (https://goo.gl/pxwQGp)
  const toType = object => {
    if (object === null || object === undefined) {
      return `${object}`;
    }
    return Object.prototype.toString.call(object).match(/\s([a-z]+)/i)[1].toLowerCase();
  };

  /**
   * Public Util API
   */

  const getUID = prefix => {
    do {
      prefix += Math.floor(Math.random() * MAX_UID);
    } while (document.getElementById(prefix));
    return prefix;
  };
  const getTransitionDurationFromElement = element => {
    if (!element) {
      return 0;
    }

    // Get transition-duration of the element
    let {
      transitionDuration,
      transitionDelay
    } = window.getComputedStyle(element);
    const floatTransitionDuration = Number.parseFloat(transitionDuration);
    const floatTransitionDelay = Number.parseFloat(transitionDelay);

    // Return 0 if element or transition duration is not found
    if (!floatTransitionDuration && !floatTransitionDelay) {
      return 0;
    }

    // If multiple durations are defined, take the first
    transitionDuration = transitionDuration.split(',')[0];
    transitionDelay = transitionDelay.split(',')[0];
    return (Number.parseFloat(transitionDuration) + Number.parseFloat(transitionDelay)) * MILLISECONDS_MULTIPLIER;
  };
  const triggerTransitionEnd = element => {
    element.dispatchEvent(new Event(TRANSITION_END));
  };
  const isElement$1 = object => {
    if (!object || typeof object !== 'object') {
      return false;
    }
    if (typeof object.jquery !== 'undefined') {
      object = object[0];
    }
    return typeof object.nodeType !== 'undefined';
  };
  const getElement = object => {
    // it's a jQuery object or a node element
    if (isElement$1(object)) {
      return object.jquery ? object[0] : object;
    }
    if (typeof object === 'string' && object.length > 0) {
      return document.querySelector(parseSelector(object));
    }
    return null;
  };
  const isVisible = element => {
    if (!isElement$1(element) || element.getClientRects().length === 0) {
      return false;
    }
    const elementIsVisible = getComputedStyle(element).getPropertyValue('visibility') === 'visible';
    // Handle `details` element as its content may falsie appear visible when it is closed
    const closedDetails = element.closest('details:not([open])');
    if (!closedDetails) {
      return elementIsVisible;
    }
    if (closedDetails !== element) {
      const summary = element.closest('summary');
      if (summary && summary.parentNode !== closedDetails) {
        return false;
      }
      if (summary === null) {
        return false;
      }
    }
    return elementIsVisible;
  };
  const isDisabled = element => {
    if (!element || element.nodeType !== Node.ELEMENT_NODE) {
      return true;
    }
    if (element.classList.contains('disabled')) {
      return true;
    }
    if (typeof element.disabled !== 'undefined') {
      return element.disabled;
    }
    return element.hasAttribute('disabled') && element.getAttribute('disabled') !== 'false';
  };
  const findShadowRoot = element => {
    if (!document.documentElement.attachShadow) {
      return null;
    }

    // Can find the shadow root otherwise it'll return the document
    if (typeof element.getRootNode === 'function') {
      const root = element.getRootNode();
      return root instanceof ShadowRoot ? root : null;
    }
    if (element instanceof ShadowRoot) {
      return element;
    }

    // when we don't find a shadow root
    if (!element.parentNode) {
      return null;
    }
    return findShadowRoot(element.parentNode);
  };
  const noop = () => {};

  /**
   * Trick to restart an element's animation
   *
   * @param {HTMLElement} element
   * @return void
   *
   * @see https://www.charistheo.io/blog/2021/02/restart-a-css-animation-with-javascript/#restarting-a-css-animation
   */
  const reflow = element => {
    element.offsetHeight; // eslint-disable-line no-unused-expressions
  };
  const getjQuery = () => {
    if (window.jQuery && !document.body.hasAttribute('data-bs-no-jquery')) {
      return window.jQuery;
    }
    return null;
  };
  const DOMContentLoadedCallbacks = [];
  const onDOMContentLoaded = callback => {
    if (document.readyState === 'loading') {
      // add listener on the first call when the document is in loading state
      if (!DOMContentLoadedCallbacks.length) {
        document.addEventListener('DOMContentLoaded', () => {
          for (const callback of DOMContentLoadedCallbacks) {
            callback();
          }
        });
      }
      DOMContentLoadedCallbacks.push(callback);
    } else {
      callback();
    }
  };
  const isRTL = () => document.documentElement.dir === 'rtl';
  const defineJQueryPlugin = plugin => {
    onDOMContentLoaded(() => {
      const $ = getjQuery();
      /* istanbul ignore if */
      if ($) {
        const name = plugin.NAME;
        const JQUERY_NO_CONFLICT = $.fn[name];
        $.fn[name] = plugin.jQueryInterface;
        $.fn[name].Constructor = plugin;
        $.fn[name].noConflict = () => {
          $.fn[name] = JQUERY_NO_CONFLICT;
          return plugin.jQueryInterface;
        };
      }
    });
  };
  const execute = (possibleCallback, args = [], defaultValue = possibleCallback) => {
    return typeof possibleCallback === 'function' ? possibleCallback(...args) : defaultValue;
  };
  const executeAfterTransition = (callback, transitionElement, waitForTransition = true) => {
    if (!waitForTransition) {
      execute(callback);
      return;
    }
    const durationPadding = 5;
    const emulatedDuration = getTransitionDurationFromElement(transitionElement) + durationPadding;
    let called = false;
    const handler = ({
      target
    }) => {
      if (target !== transitionElement) {
        return;
      }
      called = true;
      transitionElement.removeEventListener(TRANSITION_END, handler);
      execute(callback);
    };
    transitionElement.addEventListener(TRANSITION_END, handler);
    setTimeout(() => {
      if (!called) {
        triggerTransitionEnd(transitionElement);
      }
    }, emulatedDuration);
  };

  /**
   * Return the previous/next element of a list.
   *
   * @param {array} list    The list of elements
   * @param activeElement   The active element
   * @param shouldGetNext   Choose to get next or previous element
   * @param isCycleAllowed
   * @return {Element|elem} The proper element
   */
  const getNextActiveElement = (list, activeElement, shouldGetNext, isCycleAllowed) => {
    const listLength = list.length;
    let index = list.indexOf(activeElement);

    // if the element does not exist in the list return an element
    // depending on the direction and if cycle is allowed
    if (index === -1) {
      return !shouldGetNext && isCycleAllowed ? list[listLength - 1] : list[0];
    }
    index += shouldGetNext ? 1 : -1;
    if (isCycleAllowed) {
      index = (index + listLength) % listLength;
    }
    return list[Math.max(0, Math.min(index, listLength - 1))];
  };

  /**
   * --------------------------------------------------------------------------
   * Bootstrap dom/event-handler.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const namespaceRegex = /[^.]*(?=\..*)\.|.*/;
  const stripNameRegex = /\..*/;
  const stripUidRegex = /::\d+$/;
  const eventRegistry = {}; // Events storage
  let uidEvent = 1;
  const customEvents = {
    mouseenter: 'mouseover',
    mouseleave: 'mouseout'
  };
  const nativeEvents = new Set(['click', 'dblclick', 'mouseup', 'mousedown', 'contextmenu', 'mousewheel', 'DOMMouseScroll', 'mouseover', 'mouseout', 'mousemove', 'selectstart', 'selectend', 'keydown', 'keypress', 'keyup', 'orientationchange', 'touchstart', 'touchmove', 'touchend', 'touchcancel', 'pointerdown', 'pointermove', 'pointerup', 'pointerleave', 'pointercancel', 'gesturestart', 'gesturechange', 'gestureend', 'focus', 'blur', 'change', 'reset', 'select', 'submit', 'focusin', 'focusout', 'load', 'unload', 'beforeunload', 'resize', 'move', 'DOMContentLoaded', 'readystatechange', 'error', 'abort', 'scroll']);

  /**
   * Private methods
   */

  function makeEventUid(element, uid) {
    return uid && `${uid}::${uidEvent++}` || element.uidEvent || uidEvent++;
  }
  function getElementEvents(element) {
    const uid = makeEventUid(element);
    element.uidEvent = uid;
    eventRegistry[uid] = eventRegistry[uid] || {};
    return eventRegistry[uid];
  }
  function bootstrapHandler(element, fn) {
    return function handler(event) {
      hydrateObj(event, {
        delegateTarget: element
      });
      if (handler.oneOff) {
        EventHandler.off(element, event.type, fn);
      }
      return fn.apply(element, [event]);
    };
  }
  function bootstrapDelegationHandler(element, selector, fn) {
    return function handler(event) {
      const domElements = element.querySelectorAll(selector);
      for (let {
        target
      } = event; target && target !== this; target = target.parentNode) {
        for (const domElement of domElements) {
          if (domElement !== target) {
            continue;
          }
          hydrateObj(event, {
            delegateTarget: target
          });
          if (handler.oneOff) {
            EventHandler.off(element, event.type, selector, fn);
          }
          return fn.apply(target, [event]);
        }
      }
    };
  }
  function findHandler(events, callable, delegationSelector = null) {
    return Object.values(events).find(event => event.callable === callable && event.delegationSelector === delegationSelector);
  }
  function normalizeParameters(originalTypeEvent, handler, delegationFunction) {
    const isDelegated = typeof handler === 'string';
    // TODO: tooltip passes `false` instead of selector, so we need to check
    const callable = isDelegated ? delegationFunction : handler || delegationFunction;
    let typeEvent = getTypeEvent(originalTypeEvent);
    if (!nativeEvents.has(typeEvent)) {
      typeEvent = originalTypeEvent;
    }
    return [isDelegated, callable, typeEvent];
  }
  function addHandler(element, originalTypeEvent, handler, delegationFunction, oneOff) {
    if (typeof originalTypeEvent !== 'string' || !element) {
      return;
    }
    let [isDelegated, callable, typeEvent] = normalizeParameters(originalTypeEvent, handler, delegationFunction);

    // in case of mouseenter or mouseleave wrap the handler within a function that checks for its DOM position
    // this prevents the handler from being dispatched the same way as mouseover or mouseout does
    if (originalTypeEvent in customEvents) {
      const wrapFunction = fn => {
        return function (event) {
          if (!event.relatedTarget || event.relatedTarget !== event.delegateTarget && !event.delegateTarget.contains(event.relatedTarget)) {
            return fn.call(this, event);
          }
        };
      };
      callable = wrapFunction(callable);
    }
    const events = getElementEvents(element);
    const handlers = events[typeEvent] || (events[typeEvent] = {});
    const previousFunction = findHandler(handlers, callable, isDelegated ? handler : null);
    if (previousFunction) {
      previousFunction.oneOff = previousFunction.oneOff && oneOff;
      return;
    }
    const uid = makeEventUid(callable, originalTypeEvent.replace(namespaceRegex, ''));
    const fn = isDelegated ? bootstrapDelegationHandler(element, handler, callable) : bootstrapHandler(element, callable);
    fn.delegationSelector = isDelegated ? handler : null;
    fn.callable = callable;
    fn.oneOff = oneOff;
    fn.uidEvent = uid;
    handlers[uid] = fn;
    element.addEventListener(typeEvent, fn, isDelegated);
  }
  function removeHandler(element, events, typeEvent, handler, delegationSelector) {
    const fn = findHandler(events[typeEvent], handler, delegationSelector);
    if (!fn) {
      return;
    }
    element.removeEventListener(typeEvent, fn, Boolean(delegationSelector));
    delete events[typeEvent][fn.uidEvent];
  }
  function removeNamespacedHandlers(element, events, typeEvent, namespace) {
    const storeElementEvent = events[typeEvent] || {};
    for (const [handlerKey, event] of Object.entries(storeElementEvent)) {
      if (handlerKey.includes(namespace)) {
        removeHandler(element, events, typeEvent, event.callable, event.delegationSelector);
      }
    }
  }
  function getTypeEvent(event) {
    // allow to get the native events from namespaced events ('click.bs.button' --> 'click')
    event = event.replace(stripNameRegex, '');
    return customEvents[event] || event;
  }
  const EventHandler = {
    on(element, event, handler, delegationFunction) {
      addHandler(element, event, handler, delegationFunction, false);
    },
    one(element, event, handler, delegationFunction) {
      addHandler(element, event, handler, delegationFunction, true);
    },
    off(element, originalTypeEvent, handler, delegationFunction) {
      if (typeof originalTypeEvent !== 'string' || !element) {
        return;
      }
      const [isDelegated, callable, typeEvent] = normalizeParameters(originalTypeEvent, handler, delegationFunction);
      const inNamespace = typeEvent !== originalTypeEvent;
      const events = getElementEvents(element);
      const storeElementEvent = events[typeEvent] || {};
      const isNamespace = originalTypeEvent.startsWith('.');
      if (typeof callable !== 'undefined') {
        // Simplest case: handler is passed, remove that listener ONLY.
        if (!Object.keys(storeElementEvent).length) {
          return;
        }
        removeHandler(element, events, typeEvent, callable, isDelegated ? handler : null);
        return;
      }
      if (isNamespace) {
        for (const elementEvent of Object.keys(events)) {
          removeNamespacedHandlers(element, events, elementEvent, originalTypeEvent.slice(1));
        }
      }
      for (const [keyHandlers, event] of Object.entries(storeElementEvent)) {
        const handlerKey = keyHandlers.replace(stripUidRegex, '');
        if (!inNamespace || originalTypeEvent.includes(handlerKey)) {
          removeHandler(element, events, typeEvent, event.callable, event.delegationSelector);
        }
      }
    },
    trigger(element, event, args) {
      if (typeof event !== 'string' || !element) {
        return null;
      }
      const $ = getjQuery();
      const typeEvent = getTypeEvent(event);
      const inNamespace = event !== typeEvent;
      let jQueryEvent = null;
      let bubbles = true;
      let nativeDispatch = true;
      let defaultPrevented = false;
      if (inNamespace && $) {
        jQueryEvent = $.Event(event, args);
        $(element).trigger(jQueryEvent);
        bubbles = !jQueryEvent.isPropagationStopped();
        nativeDispatch = !jQueryEvent.isImmediatePropagationStopped();
        defaultPrevented = jQueryEvent.isDefaultPrevented();
      }
      const evt = hydrateObj(new Event(event, {
        bubbles,
        cancelable: true
      }), args);
      if (defaultPrevented) {
        evt.preventDefault();
      }
      if (nativeDispatch) {
        element.dispatchEvent(evt);
      }
      if (evt.defaultPrevented && jQueryEvent) {
        jQueryEvent.preventDefault();
      }
      return evt;
    }
  };
  function hydrateObj(obj, meta = {}) {
    for (const [key, value] of Object.entries(meta)) {
      try {
        obj[key] = value;
      } catch (_unused) {
        Object.defineProperty(obj, key, {
          configurable: true,
          get() {
            return value;
          }
        });
      }
    }
    return obj;
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap dom/manipulator.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */

  function normalizeData(value) {
    if (value === 'true') {
      return true;
    }
    if (value === 'false') {
      return false;
    }
    if (value === Number(value).toString()) {
      return Number(value);
    }
    if (value === '' || value === 'null') {
      return null;
    }
    if (typeof value !== 'string') {
      return value;
    }
    try {
      return JSON.parse(decodeURIComponent(value));
    } catch (_unused) {
      return value;
    }
  }
  function normalizeDataKey(key) {
    return key.replace(/[A-Z]/g, chr => `-${chr.toLowerCase()}`);
  }
  const Manipulator = {
    setDataAttribute(element, key, value) {
      element.setAttribute(`data-bs-${normalizeDataKey(key)}`, value);
    },
    removeDataAttribute(element, key) {
      element.removeAttribute(`data-bs-${normalizeDataKey(key)}`);
    },
    getDataAttributes(element) {
      if (!element) {
        return {};
      }
      const attributes = {};
      const bsKeys = Object.keys(element.dataset).filter(key => key.startsWith('bs') && !key.startsWith('bsConfig'));
      for (const key of bsKeys) {
        let pureKey = key.replace(/^bs/, '');
        pureKey = pureKey.charAt(0).toLowerCase() + pureKey.slice(1, pureKey.length);
        attributes[pureKey] = normalizeData(element.dataset[key]);
      }
      return attributes;
    },
    getDataAttribute(element, key) {
      return normalizeData(element.getAttribute(`data-bs-${normalizeDataKey(key)}`));
    }
  };

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/config.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Class definition
   */

  class Config {
    // Getters
    static get Default() {
      return {};
    }
    static get DefaultType() {
      return {};
    }
    static get NAME() {
      throw new Error('You have to implement the static method "NAME", for each component!');
    }
    _getConfig(config) {
      config = this._mergeConfigObj(config);
      config = this._configAfterMerge(config);
      this._typeCheckConfig(config);
      return config;
    }
    _configAfterMerge(config) {
      return config;
    }
    _mergeConfigObj(config, element) {
      const jsonConfig = isElement$1(element) ? Manipulator.getDataAttribute(element, 'config') : {}; // try to parse

      return {
        ...this.constructor.Default,
        ...(typeof jsonConfig === 'object' ? jsonConfig : {}),
        ...(isElement$1(element) ? Manipulator.getDataAttributes(element) : {}),
        ...(typeof config === 'object' ? config : {})
      };
    }
    _typeCheckConfig(config, configTypes = this.constructor.DefaultType) {
      for (const [property, expectedTypes] of Object.entries(configTypes)) {
        const value = config[property];
        const valueType = isElement$1(value) ? 'element' : toType(value);
        if (!new RegExp(expectedTypes).test(valueType)) {
          throw new TypeError(`${this.constructor.NAME.toUpperCase()}: Option "${property}" provided type "${valueType}" but expected type "${expectedTypes}".`);
        }
      }
    }
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap base-component.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const VERSION = '5.3.3';

  /**
   * Class definition
   */

  class BaseComponent extends Config {
    constructor(element, config) {
      super();
      element = getElement(element);
      if (!element) {
        return;
      }
      this._element = element;
      this._config = this._getConfig(config);
      Data.set(this._element, this.constructor.DATA_KEY, this);
    }

    // Public
    dispose() {
      Data.remove(this._element, this.constructor.DATA_KEY);
      EventHandler.off(this._element, this.constructor.EVENT_KEY);
      for (const propertyName of Object.getOwnPropertyNames(this)) {
        this[propertyName] = null;
      }
    }
    _queueCallback(callback, element, isAnimated = true) {
      executeAfterTransition(callback, element, isAnimated);
    }
    _getConfig(config) {
      config = this._mergeConfigObj(config, this._element);
      config = this._configAfterMerge(config);
      this._typeCheckConfig(config);
      return config;
    }

    // Static
    static getInstance(element) {
      return Data.get(getElement(element), this.DATA_KEY);
    }
    static getOrCreateInstance(element, config = {}) {
      return this.getInstance(element) || new this(element, typeof config === 'object' ? config : null);
    }
    static get VERSION() {
      return VERSION;
    }
    static get DATA_KEY() {
      return `bs.${this.NAME}`;
    }
    static get EVENT_KEY() {
      return `.${this.DATA_KEY}`;
    }
    static eventName(name) {
      return `${name}${this.EVENT_KEY}`;
    }
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap dom/selector-engine.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */

  const getSelector = element => {
    let selector = element.getAttribute('data-bs-target');
    if (!selector || selector === '#') {
      let hrefAttribute = element.getAttribute('href');

      // The only valid content that could double as a selector are IDs or classes,
      // so everything starting with `#` or `.`. If a "real" URL is used as the selector,
      // `document.querySelector` will rightfully complain it is invalid.
      // See https://github.com/twbs/bootstrap/issues/32273
      if (!hrefAttribute || !hrefAttribute.includes('#') && !hrefAttribute.startsWith('.')) {
        return null;
      }

      // Just in case some CMS puts out a full URL with the anchor appended
      if (hrefAttribute.includes('#') && !hrefAttribute.startsWith('#')) {
        hrefAttribute = `#${hrefAttribute.split('#')[1]}`;
      }
      selector = hrefAttribute && hrefAttribute !== '#' ? hrefAttribute.trim() : null;
    }
    return selector ? selector.split(',').map(sel => parseSelector(sel)).join(',') : null;
  };
  const SelectorEngine = {
    find(selector, element = document.documentElement) {
      return [].concat(...Element.prototype.querySelectorAll.call(element, selector));
    },
    findOne(selector, element = document.documentElement) {
      return Element.prototype.querySelector.call(element, selector);
    },
    children(element, selector) {
      return [].concat(...element.children).filter(child => child.matches(selector));
    },
    parents(element, selector) {
      const parents = [];
      let ancestor = element.parentNode.closest(selector);
      while (ancestor) {
        parents.push(ancestor);
        ancestor = ancestor.parentNode.closest(selector);
      }
      return parents;
    },
    prev(element, selector) {
      let previous = element.previousElementSibling;
      while (previous) {
        if (previous.matches(selector)) {
          return [previous];
        }
        previous = previous.previousElementSibling;
      }
      return [];
    },
    // TODO: this is now unused; remove later along with prev()
    next(element, selector) {
      let next = element.nextElementSibling;
      while (next) {
        if (next.matches(selector)) {
          return [next];
        }
        next = next.nextElementSibling;
      }
      return [];
    },
    focusableChildren(element) {
      const focusables = ['a', 'button', 'input', 'textarea', 'select', 'details', '[tabindex]', '[contenteditable="true"]'].map(selector => `${selector}:not([tabindex^="-"])`).join(',');
      return this.find(focusables, element).filter(el => !isDisabled(el) && isVisible(el));
    },
    getSelectorFromElement(element) {
      const selector = getSelector(element);
      if (selector) {
        return SelectorEngine.findOne(selector) ? selector : null;
      }
      return null;
    },
    getElementFromSelector(element) {
      const selector = getSelector(element);
      return selector ? SelectorEngine.findOne(selector) : null;
    },
    getMultipleElementsFromSelector(element) {
      const selector = getSelector(element);
      return selector ? SelectorEngine.find(selector) : [];
    }
  };

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/component-functions.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */

  const enableDismissTrigger = (component, method = 'hide') => {
    const clickEvent = `click.dismiss${component.EVENT_KEY}`;
    const name = component.NAME;
    EventHandler.on(document, clickEvent, `[data-bs-dismiss="${name}"]`, function (event) {
      if (['A', 'AREA'].includes(this.tagName)) {
        event.preventDefault();
      }
      if (isDisabled(this)) {
        return;
      }
      const target = SelectorEngine.getElementFromSelector(this) || this.closest(`.${name}`);
      const instance = component.getOrCreateInstance(target);

      // Method argument is left, for Alert and only, as it doesn't implement the 'hide' method
      instance[method]();
    });
  };

  /**
   * --------------------------------------------------------------------------
   * Bootstrap alert.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$f = 'alert';
  const DATA_KEY$a = 'bs.alert';
  const EVENT_KEY$b = `.${DATA_KEY$a}`;
  const EVENT_CLOSE = `close${EVENT_KEY$b}`;
  const EVENT_CLOSED = `closed${EVENT_KEY$b}`;
  const CLASS_NAME_FADE$5 = 'fade';
  const CLASS_NAME_SHOW$8 = 'show';

  /**
   * Class definition
   */

  class Alert extends BaseComponent {
    // Getters
    static get NAME() {
      return NAME$f;
    }

    // Public
    close() {
      const closeEvent = EventHandler.trigger(this._element, EVENT_CLOSE);
      if (closeEvent.defaultPrevented) {
        return;
      }
      this._element.classList.remove(CLASS_NAME_SHOW$8);
      const isAnimated = this._element.classList.contains(CLASS_NAME_FADE$5);
      this._queueCallback(() => this._destroyElement(), this._element, isAnimated);
    }

    // Private
    _destroyElement() {
      this._element.remove();
      EventHandler.trigger(this._element, EVENT_CLOSED);
      this.dispose();
    }

    // Static
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Alert.getOrCreateInstance(this);
        if (typeof config !== 'string') {
          return;
        }
        if (data[config] === undefined || config.startsWith('_') || config === 'constructor') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config](this);
      });
    }
  }

  /**
   * Data API implementation
   */

  enableDismissTrigger(Alert, 'close');

  /**
   * jQuery
   */

  defineJQueryPlugin(Alert);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap button.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$e = 'button';
  const DATA_KEY$9 = 'bs.button';
  const EVENT_KEY$a = `.${DATA_KEY$9}`;
  const DATA_API_KEY$6 = '.data-api';
  const CLASS_NAME_ACTIVE$3 = 'active';
  const SELECTOR_DATA_TOGGLE$5 = '[data-bs-toggle="button"]';
  const EVENT_CLICK_DATA_API$6 = `click${EVENT_KEY$a}${DATA_API_KEY$6}`;

  /**
   * Class definition
   */

  class Button extends BaseComponent {
    // Getters
    static get NAME() {
      return NAME$e;
    }

    // Public
    toggle() {
      // Toggle class and sync the `aria-pressed` attribute with the return value of the `.toggle()` method
      this._element.setAttribute('aria-pressed', this._element.classList.toggle(CLASS_NAME_ACTIVE$3));
    }

    // Static
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Button.getOrCreateInstance(this);
        if (config === 'toggle') {
          data[config]();
        }
      });
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(document, EVENT_CLICK_DATA_API$6, SELECTOR_DATA_TOGGLE$5, event => {
    event.preventDefault();
    const button = event.target.closest(SELECTOR_DATA_TOGGLE$5);
    const data = Button.getOrCreateInstance(button);
    data.toggle();
  });

  /**
   * jQuery
   */

  defineJQueryPlugin(Button);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/swipe.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$d = 'swipe';
  const EVENT_KEY$9 = '.bs.swipe';
  const EVENT_TOUCHSTART = `touchstart${EVENT_KEY$9}`;
  const EVENT_TOUCHMOVE = `touchmove${EVENT_KEY$9}`;
  const EVENT_TOUCHEND = `touchend${EVENT_KEY$9}`;
  const EVENT_POINTERDOWN = `pointerdown${EVENT_KEY$9}`;
  const EVENT_POINTERUP = `pointerup${EVENT_KEY$9}`;
  const POINTER_TYPE_TOUCH = 'touch';
  const POINTER_TYPE_PEN = 'pen';
  const CLASS_NAME_POINTER_EVENT = 'pointer-event';
  const SWIPE_THRESHOLD = 40;
  const Default$c = {
    endCallback: null,
    leftCallback: null,
    rightCallback: null
  };
  const DefaultType$c = {
    endCallback: '(function|null)',
    leftCallback: '(function|null)',
    rightCallback: '(function|null)'
  };

  /**
   * Class definition
   */

  class Swipe extends Config {
    constructor(element, config) {
      super();
      this._element = element;
      if (!element || !Swipe.isSupported()) {
        return;
      }
      this._config = this._getConfig(config);
      this._deltaX = 0;
      this._supportPointerEvents = Boolean(window.PointerEvent);
      this._initEvents();
    }

    // Getters
    static get Default() {
      return Default$c;
    }
    static get DefaultType() {
      return DefaultType$c;
    }
    static get NAME() {
      return NAME$d;
    }

    // Public
    dispose() {
      EventHandler.off(this._element, EVENT_KEY$9);
    }

    // Private
    _start(event) {
      if (!this._supportPointerEvents) {
        this._deltaX = event.touches[0].clientX;
        return;
      }
      if (this._eventIsPointerPenTouch(event)) {
        this._deltaX = event.clientX;
      }
    }
    _end(event) {
      if (this._eventIsPointerPenTouch(event)) {
        this._deltaX = event.clientX - this._deltaX;
      }
      this._handleSwipe();
      execute(this._config.endCallback);
    }
    _move(event) {
      this._deltaX = event.touches && event.touches.length > 1 ? 0 : event.touches[0].clientX - this._deltaX;
    }
    _handleSwipe() {
      const absDeltaX = Math.abs(this._deltaX);
      if (absDeltaX <= SWIPE_THRESHOLD) {
        return;
      }
      const direction = absDeltaX / this._deltaX;
      this._deltaX = 0;
      if (!direction) {
        return;
      }
      execute(direction > 0 ? this._config.rightCallback : this._config.leftCallback);
    }
    _initEvents() {
      if (this._supportPointerEvents) {
        EventHandler.on(this._element, EVENT_POINTERDOWN, event => this._start(event));
        EventHandler.on(this._element, EVENT_POINTERUP, event => this._end(event));
        this._element.classList.add(CLASS_NAME_POINTER_EVENT);
      } else {
        EventHandler.on(this._element, EVENT_TOUCHSTART, event => this._start(event));
        EventHandler.on(this._element, EVENT_TOUCHMOVE, event => this._move(event));
        EventHandler.on(this._element, EVENT_TOUCHEND, event => this._end(event));
      }
    }
    _eventIsPointerPenTouch(event) {
      return this._supportPointerEvents && (event.pointerType === POINTER_TYPE_PEN || event.pointerType === POINTER_TYPE_TOUCH);
    }

    // Static
    static isSupported() {
      return 'ontouchstart' in document.documentElement || navigator.maxTouchPoints > 0;
    }
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap carousel.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$c = 'carousel';
  const DATA_KEY$8 = 'bs.carousel';
  const EVENT_KEY$8 = `.${DATA_KEY$8}`;
  const DATA_API_KEY$5 = '.data-api';
  const ARROW_LEFT_KEY$1 = 'ArrowLeft';
  const ARROW_RIGHT_KEY$1 = 'ArrowRight';
  const TOUCHEVENT_COMPAT_WAIT = 500; // Time for mouse compat events to fire after touch

  const ORDER_NEXT = 'next';
  const ORDER_PREV = 'prev';
  const DIRECTION_LEFT = 'left';
  const DIRECTION_RIGHT = 'right';
  const EVENT_SLIDE = `slide${EVENT_KEY$8}`;
  const EVENT_SLID = `slid${EVENT_KEY$8}`;
  const EVENT_KEYDOWN$1 = `keydown${EVENT_KEY$8}`;
  const EVENT_MOUSEENTER$1 = `mouseenter${EVENT_KEY$8}`;
  const EVENT_MOUSELEAVE$1 = `mouseleave${EVENT_KEY$8}`;
  const EVENT_DRAG_START = `dragstart${EVENT_KEY$8}`;
  const EVENT_LOAD_DATA_API$3 = `load${EVENT_KEY$8}${DATA_API_KEY$5}`;
  const EVENT_CLICK_DATA_API$5 = `click${EVENT_KEY$8}${DATA_API_KEY$5}`;
  const CLASS_NAME_CAROUSEL = 'carousel';
  const CLASS_NAME_ACTIVE$2 = 'active';
  const CLASS_NAME_SLIDE = 'slide';
  const CLASS_NAME_END = 'carousel-item-end';
  const CLASS_NAME_START = 'carousel-item-start';
  const CLASS_NAME_NEXT = 'carousel-item-next';
  const CLASS_NAME_PREV = 'carousel-item-prev';
  const SELECTOR_ACTIVE = '.active';
  const SELECTOR_ITEM = '.carousel-item';
  const SELECTOR_ACTIVE_ITEM = SELECTOR_ACTIVE + SELECTOR_ITEM;
  const SELECTOR_ITEM_IMG = '.carousel-item img';
  const SELECTOR_INDICATORS = '.carousel-indicators';
  const SELECTOR_DATA_SLIDE = '[data-bs-slide], [data-bs-slide-to]';
  const SELECTOR_DATA_RIDE = '[data-bs-ride="carousel"]';
  const KEY_TO_DIRECTION = {
    [ARROW_LEFT_KEY$1]: DIRECTION_RIGHT,
    [ARROW_RIGHT_KEY$1]: DIRECTION_LEFT
  };
  const Default$b = {
    interval: 5000,
    keyboard: true,
    pause: 'hover',
    ride: false,
    touch: true,
    wrap: true
  };
  const DefaultType$b = {
    interval: '(number|boolean)',
    // TODO:v6 remove boolean support
    keyboard: 'boolean',
    pause: '(string|boolean)',
    ride: '(boolean|string)',
    touch: 'boolean',
    wrap: 'boolean'
  };

  /**
   * Class definition
   */

  class Carousel extends BaseComponent {
    constructor(element, config) {
      super(element, config);
      this._interval = null;
      this._activeElement = null;
      this._isSliding = false;
      this.touchTimeout = null;
      this._swipeHelper = null;
      this._indicatorsElement = SelectorEngine.findOne(SELECTOR_INDICATORS, this._element);
      this._addEventListeners();
      if (this._config.ride === CLASS_NAME_CAROUSEL) {
        this.cycle();
      }
    }

    // Getters
    static get Default() {
      return Default$b;
    }
    static get DefaultType() {
      return DefaultType$b;
    }
    static get NAME() {
      return NAME$c;
    }

    // Public
    next() {
      this._slide(ORDER_NEXT);
    }
    nextWhenVisible() {
      // FIXME TODO use `document.visibilityState`
      // Don't call next when the page isn't visible
      // or the carousel or its parent isn't visible
      if (!document.hidden && isVisible(this._element)) {
        this.next();
      }
    }
    prev() {
      this._slide(ORDER_PREV);
    }
    pause() {
      if (this._isSliding) {
        triggerTransitionEnd(this._element);
      }
      this._clearInterval();
    }
    cycle() {
      this._clearInterval();
      this._updateInterval();
      this._interval = setInterval(() => this.nextWhenVisible(), this._config.interval);
    }
    _maybeEnableCycle() {
      if (!this._config.ride) {
        return;
      }
      if (this._isSliding) {
        EventHandler.one(this._element, EVENT_SLID, () => this.cycle());
        return;
      }
      this.cycle();
    }
    to(index) {
      const items = this._getItems();
      if (index > items.length - 1 || index < 0) {
        return;
      }
      if (this._isSliding) {
        EventHandler.one(this._element, EVENT_SLID, () => this.to(index));
        return;
      }
      const activeIndex = this._getItemIndex(this._getActive());
      if (activeIndex === index) {
        return;
      }
      const order = index > activeIndex ? ORDER_NEXT : ORDER_PREV;
      this._slide(order, items[index]);
    }
    dispose() {
      if (this._swipeHelper) {
        this._swipeHelper.dispose();
      }
      super.dispose();
    }

    // Private
    _configAfterMerge(config) {
      config.defaultInterval = config.interval;
      return config;
    }
    _addEventListeners() {
      if (this._config.keyboard) {
        EventHandler.on(this._element, EVENT_KEYDOWN$1, event => this._keydown(event));
      }
      if (this._config.pause === 'hover') {
        EventHandler.on(this._element, EVENT_MOUSEENTER$1, () => this.pause());
        EventHandler.on(this._element, EVENT_MOUSELEAVE$1, () => this._maybeEnableCycle());
      }
      if (this._config.touch && Swipe.isSupported()) {
        this._addTouchEventListeners();
      }
    }
    _addTouchEventListeners() {
      for (const img of SelectorEngine.find(SELECTOR_ITEM_IMG, this._element)) {
        EventHandler.on(img, EVENT_DRAG_START, event => event.preventDefault());
      }
      const endCallBack = () => {
        if (this._config.pause !== 'hover') {
          return;
        }

        // If it's a touch-enabled device, mouseenter/leave are fired as
        // part of the mouse compatibility events on first tap - the carousel
        // would stop cycling until user tapped out of it;
        // here, we listen for touchend, explicitly pause the carousel
        // (as if it's the second time we tap on it, mouseenter compat event
        // is NOT fired) and after a timeout (to allow for mouse compatibility
        // events to fire) we explicitly restart cycling

        this.pause();
        if (this.touchTimeout) {
          clearTimeout(this.touchTimeout);
        }
        this.touchTimeout = setTimeout(() => this._maybeEnableCycle(), TOUCHEVENT_COMPAT_WAIT + this._config.interval);
      };
      const swipeConfig = {
        leftCallback: () => this._slide(this._directionToOrder(DIRECTION_LEFT)),
        rightCallback: () => this._slide(this._directionToOrder(DIRECTION_RIGHT)),
        endCallback: endCallBack
      };
      this._swipeHelper = new Swipe(this._element, swipeConfig);
    }
    _keydown(event) {
      if (/input|textarea/i.test(event.target.tagName)) {
        return;
      }
      const direction = KEY_TO_DIRECTION[event.key];
      if (direction) {
        event.preventDefault();
        this._slide(this._directionToOrder(direction));
      }
    }
    _getItemIndex(element) {
      return this._getItems().indexOf(element);
    }
    _setActiveIndicatorElement(index) {
      if (!this._indicatorsElement) {
        return;
      }
      const activeIndicator = SelectorEngine.findOne(SELECTOR_ACTIVE, this._indicatorsElement);
      activeIndicator.classList.remove(CLASS_NAME_ACTIVE$2);
      activeIndicator.removeAttribute('aria-current');
      const newActiveIndicator = SelectorEngine.findOne(`[data-bs-slide-to="${index}"]`, this._indicatorsElement);
      if (newActiveIndicator) {
        newActiveIndicator.classList.add(CLASS_NAME_ACTIVE$2);
        newActiveIndicator.setAttribute('aria-current', 'true');
      }
    }
    _updateInterval() {
      const element = this._activeElement || this._getActive();
      if (!element) {
        return;
      }
      const elementInterval = Number.parseInt(element.getAttribute('data-bs-interval'), 10);
      this._config.interval = elementInterval || this._config.defaultInterval;
    }
    _slide(order, element = null) {
      if (this._isSliding) {
        return;
      }
      const activeElement = this._getActive();
      const isNext = order === ORDER_NEXT;
      const nextElement = element || getNextActiveElement(this._getItems(), activeElement, isNext, this._config.wrap);
      if (nextElement === activeElement) {
        return;
      }
      const nextElementIndex = this._getItemIndex(nextElement);
      const triggerEvent = eventName => {
        return EventHandler.trigger(this._element, eventName, {
          relatedTarget: nextElement,
          direction: this._orderToDirection(order),
          from: this._getItemIndex(activeElement),
          to: nextElementIndex
        });
      };
      const slideEvent = triggerEvent(EVENT_SLIDE);
      if (slideEvent.defaultPrevented) {
        return;
      }
      if (!activeElement || !nextElement) {
        // Some weirdness is happening, so we bail
        // TODO: change tests that use empty divs to avoid this check
        return;
      }
      const isCycling = Boolean(this._interval);
      this.pause();
      this._isSliding = true;
      this._setActiveIndicatorElement(nextElementIndex);
      this._activeElement = nextElement;
      const directionalClassName = isNext ? CLASS_NAME_START : CLASS_NAME_END;
      const orderClassName = isNext ? CLASS_NAME_NEXT : CLASS_NAME_PREV;
      nextElement.classList.add(orderClassName);
      reflow(nextElement);
      activeElement.classList.add(directionalClassName);
      nextElement.classList.add(directionalClassName);
      const completeCallBack = () => {
        nextElement.classList.remove(directionalClassName, orderClassName);
        nextElement.classList.add(CLASS_NAME_ACTIVE$2);
        activeElement.classList.remove(CLASS_NAME_ACTIVE$2, orderClassName, directionalClassName);
        this._isSliding = false;
        triggerEvent(EVENT_SLID);
      };
      this._queueCallback(completeCallBack, activeElement, this._isAnimated());
      if (isCycling) {
        this.cycle();
      }
    }
    _isAnimated() {
      return this._element.classList.contains(CLASS_NAME_SLIDE);
    }
    _getActive() {
      return SelectorEngine.findOne(SELECTOR_ACTIVE_ITEM, this._element);
    }
    _getItems() {
      return SelectorEngine.find(SELECTOR_ITEM, this._element);
    }
    _clearInterval() {
      if (this._interval) {
        clearInterval(this._interval);
        this._interval = null;
      }
    }
    _directionToOrder(direction) {
      if (isRTL()) {
        return direction === DIRECTION_LEFT ? ORDER_PREV : ORDER_NEXT;
      }
      return direction === DIRECTION_LEFT ? ORDER_NEXT : ORDER_PREV;
    }
    _orderToDirection(order) {
      if (isRTL()) {
        return order === ORDER_PREV ? DIRECTION_LEFT : DIRECTION_RIGHT;
      }
      return order === ORDER_PREV ? DIRECTION_RIGHT : DIRECTION_LEFT;
    }

    // Static
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Carousel.getOrCreateInstance(this, config);
        if (typeof config === 'number') {
          data.to(config);
          return;
        }
        if (typeof config === 'string') {
          if (data[config] === undefined || config.startsWith('_') || config === 'constructor') {
            throw new TypeError(`No method named "${config}"`);
          }
          data[config]();
        }
      });
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(document, EVENT_CLICK_DATA_API$5, SELECTOR_DATA_SLIDE, function (event) {
    const target = SelectorEngine.getElementFromSelector(this);
    if (!target || !target.classList.contains(CLASS_NAME_CAROUSEL)) {
      return;
    }
    event.preventDefault();
    const carousel = Carousel.getOrCreateInstance(target);
    const slideIndex = this.getAttribute('data-bs-slide-to');
    if (slideIndex) {
      carousel.to(slideIndex);
      carousel._maybeEnableCycle();
      return;
    }
    if (Manipulator.getDataAttribute(this, 'slide') === 'next') {
      carousel.next();
      carousel._maybeEnableCycle();
      return;
    }
    carousel.prev();
    carousel._maybeEnableCycle();
  });
  EventHandler.on(window, EVENT_LOAD_DATA_API$3, () => {
    const carousels = SelectorEngine.find(SELECTOR_DATA_RIDE);
    for (const carousel of carousels) {
      Carousel.getOrCreateInstance(carousel);
    }
  });

  /**
   * jQuery
   */

  defineJQueryPlugin(Carousel);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap collapse.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$b = 'collapse';
  const DATA_KEY$7 = 'bs.collapse';
  const EVENT_KEY$7 = `.${DATA_KEY$7}`;
  const DATA_API_KEY$4 = '.data-api';
  const EVENT_SHOW$6 = `show${EVENT_KEY$7}`;
  const EVENT_SHOWN$6 = `shown${EVENT_KEY$7}`;
  const EVENT_HIDE$6 = `hide${EVENT_KEY$7}`;
  const EVENT_HIDDEN$6 = `hidden${EVENT_KEY$7}`;
  const EVENT_CLICK_DATA_API$4 = `click${EVENT_KEY$7}${DATA_API_KEY$4}`;
  const CLASS_NAME_SHOW$7 = 'show';
  const CLASS_NAME_COLLAPSE = 'collapse';
  const CLASS_NAME_COLLAPSING = 'collapsing';
  const CLASS_NAME_COLLAPSED = 'collapsed';
  const CLASS_NAME_DEEPER_CHILDREN = `:scope .${CLASS_NAME_COLLAPSE} .${CLASS_NAME_COLLAPSE}`;
  const CLASS_NAME_HORIZONTAL = 'collapse-horizontal';
  const WIDTH = 'width';
  const HEIGHT = 'height';
  const SELECTOR_ACTIVES = '.collapse.show, .collapse.collapsing';
  const SELECTOR_DATA_TOGGLE$4 = '[data-bs-toggle="collapse"]';
  const Default$a = {
    parent: null,
    toggle: true
  };
  const DefaultType$a = {
    parent: '(null|element)',
    toggle: 'boolean'
  };

  /**
   * Class definition
   */

  class Collapse extends BaseComponent {
    constructor(element, config) {
      super(element, config);
      this._isTransitioning = false;
      this._triggerArray = [];
      const toggleList = SelectorEngine.find(SELECTOR_DATA_TOGGLE$4);
      for (const elem of toggleList) {
        const selector = SelectorEngine.getSelectorFromElement(elem);
        const filterElement = SelectorEngine.find(selector).filter(foundElement => foundElement === this._element);
        if (selector !== null && filterElement.length) {
          this._triggerArray.push(elem);
        }
      }
      this._initializeChildren();
      if (!this._config.parent) {
        this._addAriaAndCollapsedClass(this._triggerArray, this._isShown());
      }
      if (this._config.toggle) {
        this.toggle();
      }
    }

    // Getters
    static get Default() {
      return Default$a;
    }
    static get DefaultType() {
      return DefaultType$a;
    }
    static get NAME() {
      return NAME$b;
    }

    // Public
    toggle() {
      if (this._isShown()) {
        this.hide();
      } else {
        this.show();
      }
    }
    show() {
      if (this._isTransitioning || this._isShown()) {
        return;
      }
      let activeChildren = [];

      // find active children
      if (this._config.parent) {
        activeChildren = this._getFirstLevelChildren(SELECTOR_ACTIVES).filter(element => element !== this._element).map(element => Collapse.getOrCreateInstance(element, {
          toggle: false
        }));
      }
      if (activeChildren.length && activeChildren[0]._isTransitioning) {
        return;
      }
      const startEvent = EventHandler.trigger(this._element, EVENT_SHOW$6);
      if (startEvent.defaultPrevented) {
        return;
      }
      for (const activeInstance of activeChildren) {
        activeInstance.hide();
      }
      const dimension = this._getDimension();
      this._element.classList.remove(CLASS_NAME_COLLAPSE);
      this._element.classList.add(CLASS_NAME_COLLAPSING);
      this._element.style[dimension] = 0;
      this._addAriaAndCollapsedClass(this._triggerArray, true);
      this._isTransitioning = true;
      const complete = () => {
        this._isTransitioning = false;
        this._element.classList.remove(CLASS_NAME_COLLAPSING);
        this._element.classList.add(CLASS_NAME_COLLAPSE, CLASS_NAME_SHOW$7);
        this._element.style[dimension] = '';
        EventHandler.trigger(this._element, EVENT_SHOWN$6);
      };
      const capitalizedDimension = dimension[0].toUpperCase() + dimension.slice(1);
      const scrollSize = `scroll${capitalizedDimension}`;
      this._queueCallback(complete, this._element, true);
      this._element.style[dimension] = `${this._element[scrollSize]}px`;
    }
    hide() {
      if (this._isTransitioning || !this._isShown()) {
        return;
      }
      const startEvent = EventHandler.trigger(this._element, EVENT_HIDE$6);
      if (startEvent.defaultPrevented) {
        return;
      }
      const dimension = this._getDimension();
      this._element.style[dimension] = `${this._element.getBoundingClientRect()[dimension]}px`;
      reflow(this._element);
      this._element.classList.add(CLASS_NAME_COLLAPSING);
      this._element.classList.remove(CLASS_NAME_COLLAPSE, CLASS_NAME_SHOW$7);
      for (const trigger of this._triggerArray) {
        const element = SelectorEngine.getElementFromSelector(trigger);
        if (element && !this._isShown(element)) {
          this._addAriaAndCollapsedClass([trigger], false);
        }
      }
      this._isTransitioning = true;
      const complete = () => {
        this._isTransitioning = false;
        this._element.classList.remove(CLASS_NAME_COLLAPSING);
        this._element.classList.add(CLASS_NAME_COLLAPSE);
        EventHandler.trigger(this._element, EVENT_HIDDEN$6);
      };
      this._element.style[dimension] = '';
      this._queueCallback(complete, this._element, true);
    }
    _isShown(element = this._element) {
      return element.classList.contains(CLASS_NAME_SHOW$7);
    }

    // Private
    _configAfterMerge(config) {
      config.toggle = Boolean(config.toggle); // Coerce string values
      config.parent = getElement(config.parent);
      return config;
    }
    _getDimension() {
      return this._element.classList.contains(CLASS_NAME_HORIZONTAL) ? WIDTH : HEIGHT;
    }
    _initializeChildren() {
      if (!this._config.parent) {
        return;
      }
      const children = this._getFirstLevelChildren(SELECTOR_DATA_TOGGLE$4);
      for (const element of children) {
        const selected = SelectorEngine.getElementFromSelector(element);
        if (selected) {
          this._addAriaAndCollapsedClass([element], this._isShown(selected));
        }
      }
    }
    _getFirstLevelChildren(selector) {
      const children = SelectorEngine.find(CLASS_NAME_DEEPER_CHILDREN, this._config.parent);
      // remove children if greater depth
      return SelectorEngine.find(selector, this._config.parent).filter(element => !children.includes(element));
    }
    _addAriaAndCollapsedClass(triggerArray, isOpen) {
      if (!triggerArray.length) {
        return;
      }
      for (const element of triggerArray) {
        element.classList.toggle(CLASS_NAME_COLLAPSED, !isOpen);
        element.setAttribute('aria-expanded', isOpen);
      }
    }

    // Static
    static jQueryInterface(config) {
      const _config = {};
      if (typeof config === 'string' && /show|hide/.test(config)) {
        _config.toggle = false;
      }
      return this.each(function () {
        const data = Collapse.getOrCreateInstance(this, _config);
        if (typeof config === 'string') {
          if (typeof data[config] === 'undefined') {
            throw new TypeError(`No method named "${config}"`);
          }
          data[config]();
        }
      });
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(document, EVENT_CLICK_DATA_API$4, SELECTOR_DATA_TOGGLE$4, function (event) {
    // preventDefault only for <a> elements (which change the URL) not inside the collapsible element
    if (event.target.tagName === 'A' || event.delegateTarget && event.delegateTarget.tagName === 'A') {
      event.preventDefault();
    }
    for (const element of SelectorEngine.getMultipleElementsFromSelector(this)) {
      Collapse.getOrCreateInstance(element, {
        toggle: false
      }).toggle();
    }
  });

  /**
   * jQuery
   */

  defineJQueryPlugin(Collapse);

  var top = 'top';
  var bottom = 'bottom';
  var right = 'right';
  var left = 'left';
  var auto = 'auto';
  var basePlacements = [top, bottom, right, left];
  var start = 'start';
  var end = 'end';
  var clippingParents = 'clippingParents';
  var viewport = 'viewport';
  var popper = 'popper';
  var reference = 'reference';
  var variationPlacements = /*#__PURE__*/basePlacements.reduce(function (acc, placement) {
    return acc.concat([placement + "-" + start, placement + "-" + end]);
  }, []);
  var placements = /*#__PURE__*/[].concat(basePlacements, [auto]).reduce(function (acc, placement) {
    return acc.concat([placement, placement + "-" + start, placement + "-" + end]);
  }, []); // modifiers that need to read the DOM

  var beforeRead = 'beforeRead';
  var read = 'read';
  var afterRead = 'afterRead'; // pure-logic modifiers

  var beforeMain = 'beforeMain';
  var main = 'main';
  var afterMain = 'afterMain'; // modifier with the purpose to write to the DOM (or write into a framework state)

  var beforeWrite = 'beforeWrite';
  var write = 'write';
  var afterWrite = 'afterWrite';
  var modifierPhases = [beforeRead, read, afterRead, beforeMain, main, afterMain, beforeWrite, write, afterWrite];

  function getNodeName(element) {
    return element ? (element.nodeName || '').toLowerCase() : null;
  }

  function getWindow(node) {
    if (node == null) {
      return window;
    }

    if (node.toString() !== '[object Window]') {
      var ownerDocument = node.ownerDocument;
      return ownerDocument ? ownerDocument.defaultView || window : window;
    }

    return node;
  }

  function isElement(node) {
    var OwnElement = getWindow(node).Element;
    return node instanceof OwnElement || node instanceof Element;
  }

  function isHTMLElement(node) {
    var OwnElement = getWindow(node).HTMLElement;
    return node instanceof OwnElement || node instanceof HTMLElement;
  }

  function isShadowRoot(node) {
    // IE 11 has no ShadowRoot
    if (typeof ShadowRoot === 'undefined') {
      return false;
    }

    var OwnElement = getWindow(node).ShadowRoot;
    return node instanceof OwnElement || node instanceof ShadowRoot;
  }

  // and applies them to the HTMLElements such as popper and arrow

  function applyStyles(_ref) {
    var state = _ref.state;
    Object.keys(state.elements).forEach(function (name) {
      var style = state.styles[name] || {};
      var attributes = state.attributes[name] || {};
      var element = state.elements[name]; // arrow is optional + virtual elements

      if (!isHTMLElement(element) || !getNodeName(element)) {
        return;
      } // Flow doesn't support to extend this property, but it's the most
      // effective way to apply styles to an HTMLElement
      // $FlowFixMe[cannot-write]


      Object.assign(element.style, style);
      Object.keys(attributes).forEach(function (name) {
        var value = attributes[name];

        if (value === false) {
          element.removeAttribute(name);
        } else {
          element.setAttribute(name, value === true ? '' : value);
        }
      });
    });
  }

  function effect$2(_ref2) {
    var state = _ref2.state;
    var initialStyles = {
      popper: {
        position: state.options.strategy,
        left: '0',
        top: '0',
        margin: '0'
      },
      arrow: {
        position: 'absolute'
      },
      reference: {}
    };
    Object.assign(state.elements.popper.style, initialStyles.popper);
    state.styles = initialStyles;

    if (state.elements.arrow) {
      Object.assign(state.elements.arrow.style, initialStyles.arrow);
    }

    return function () {
      Object.keys(state.elements).forEach(function (name) {
        var element = state.elements[name];
        var attributes = state.attributes[name] || {};
        var styleProperties = Object.keys(state.styles.hasOwnProperty(name) ? state.styles[name] : initialStyles[name]); // Set all values to an empty string to unset them

        var style = styleProperties.reduce(function (style, property) {
          style[property] = '';
          return style;
        }, {}); // arrow is optional + virtual elements

        if (!isHTMLElement(element) || !getNodeName(element)) {
          return;
        }

        Object.assign(element.style, style);
        Object.keys(attributes).forEach(function (attribute) {
          element.removeAttribute(attribute);
        });
      });
    };
  } // eslint-disable-next-line import/no-unused-modules


  const applyStyles$1 = {
    name: 'applyStyles',
    enabled: true,
    phase: 'write',
    fn: applyStyles,
    effect: effect$2,
    requires: ['computeStyles']
  };

  function getBasePlacement(placement) {
    return placement.split('-')[0];
  }

  var max = Math.max;
  var min = Math.min;
  var round = Math.round;

  function getUAString() {
    var uaData = navigator.userAgentData;

    if (uaData != null && uaData.brands && Array.isArray(uaData.brands)) {
      return uaData.brands.map(function (item) {
        return item.brand + "/" + item.version;
      }).join(' ');
    }

    return navigator.userAgent;
  }

  function isLayoutViewport() {
    return !/^((?!chrome|android).)*safari/i.test(getUAString());
  }

  function getBoundingClientRect(element, includeScale, isFixedStrategy) {
    if (includeScale === void 0) {
      includeScale = false;
    }

    if (isFixedStrategy === void 0) {
      isFixedStrategy = false;
    }

    var clientRect = element.getBoundingClientRect();
    var scaleX = 1;
    var scaleY = 1;

    if (includeScale && isHTMLElement(element)) {
      scaleX = element.offsetWidth > 0 ? round(clientRect.width) / element.offsetWidth || 1 : 1;
      scaleY = element.offsetHeight > 0 ? round(clientRect.height) / element.offsetHeight || 1 : 1;
    }

    var _ref = isElement(element) ? getWindow(element) : window,
        visualViewport = _ref.visualViewport;

    var addVisualOffsets = !isLayoutViewport() && isFixedStrategy;
    var x = (clientRect.left + (addVisualOffsets && visualViewport ? visualViewport.offsetLeft : 0)) / scaleX;
    var y = (clientRect.top + (addVisualOffsets && visualViewport ? visualViewport.offsetTop : 0)) / scaleY;
    var width = clientRect.width / scaleX;
    var height = clientRect.height / scaleY;
    return {
      width: width,
      height: height,
      top: y,
      right: x + width,
      bottom: y + height,
      left: x,
      x: x,
      y: y
    };
  }

  // means it doesn't take into account transforms.

  function getLayoutRect(element) {
    var clientRect = getBoundingClientRect(element); // Use the clientRect sizes if it's not been transformed.
    // Fixes https://github.com/popperjs/popper-core/issues/1223

    var width = element.offsetWidth;
    var height = element.offsetHeight;

    if (Math.abs(clientRect.width - width) <= 1) {
      width = clientRect.width;
    }

    if (Math.abs(clientRect.height - height) <= 1) {
      height = clientRect.height;
    }

    return {
      x: element.offsetLeft,
      y: element.offsetTop,
      width: width,
      height: height
    };
  }

  function contains(parent, child) {
    var rootNode = child.getRootNode && child.getRootNode(); // First, attempt with faster native method

    if (parent.contains(child)) {
      return true;
    } // then fallback to custom implementation with Shadow DOM support
    else if (rootNode && isShadowRoot(rootNode)) {
        var next = child;

        do {
          if (next && parent.isSameNode(next)) {
            return true;
          } // $FlowFixMe[prop-missing]: need a better way to handle this...


          next = next.parentNode || next.host;
        } while (next);
      } // Give up, the result is false


    return false;
  }

  function getComputedStyle$1(element) {
    return getWindow(element).getComputedStyle(element);
  }

  function isTableElement(element) {
    return ['table', 'td', 'th'].indexOf(getNodeName(element)) >= 0;
  }

  function getDocumentElement(element) {
    // $FlowFixMe[incompatible-return]: assume body is always available
    return ((isElement(element) ? element.ownerDocument : // $FlowFixMe[prop-missing]
    element.document) || window.document).documentElement;
  }

  function getParentNode(element) {
    if (getNodeName(element) === 'html') {
      return element;
    }

    return (// this is a quicker (but less type safe) way to save quite some bytes from the bundle
      // $FlowFixMe[incompatible-return]
      // $FlowFixMe[prop-missing]
      element.assignedSlot || // step into the shadow DOM of the parent of a slotted node
      element.parentNode || ( // DOM Element detected
      isShadowRoot(element) ? element.host : null) || // ShadowRoot detected
      // $FlowFixMe[incompatible-call]: HTMLElement is a Node
      getDocumentElement(element) // fallback

    );
  }

  function getTrueOffsetParent(element) {
    if (!isHTMLElement(element) || // https://github.com/popperjs/popper-core/issues/837
    getComputedStyle$1(element).position === 'fixed') {
      return null;
    }

    return element.offsetParent;
  } // `.offsetParent` reports `null` for fixed elements, while absolute elements
  // return the containing block


  function getContainingBlock(element) {
    var isFirefox = /firefox/i.test(getUAString());
    var isIE = /Trident/i.test(getUAString());

    if (isIE && isHTMLElement(element)) {
      // In IE 9, 10 and 11 fixed elements containing block is always established by the viewport
      var elementCss = getComputedStyle$1(element);

      if (elementCss.position === 'fixed') {
        return null;
      }
    }

    var currentNode = getParentNode(element);

    if (isShadowRoot(currentNode)) {
      currentNode = currentNode.host;
    }

    while (isHTMLElement(currentNode) && ['html', 'body'].indexOf(getNodeName(currentNode)) < 0) {
      var css = getComputedStyle$1(currentNode); // This is non-exhaustive but covers the most common CSS properties that
      // create a containing block.
      // https://developer.mozilla.org/en-US/docs/Web/CSS/Containing_block#identifying_the_containing_block

      if (css.transform !== 'none' || css.perspective !== 'none' || css.contain === 'paint' || ['transform', 'perspective'].indexOf(css.willChange) !== -1 || isFirefox && css.willChange === 'filter' || isFirefox && css.filter && css.filter !== 'none') {
        return currentNode;
      } else {
        currentNode = currentNode.parentNode;
      }
    }

    return null;
  } // Gets the closest ancestor positioned element. Handles some edge cases,
  // such as table ancestors and cross browser bugs.


  function getOffsetParent(element) {
    var window = getWindow(element);
    var offsetParent = getTrueOffsetParent(element);

    while (offsetParent && isTableElement(offsetParent) && getComputedStyle$1(offsetParent).position === 'static') {
      offsetParent = getTrueOffsetParent(offsetParent);
    }

    if (offsetParent && (getNodeName(offsetParent) === 'html' || getNodeName(offsetParent) === 'body' && getComputedStyle$1(offsetParent).position === 'static')) {
      return window;
    }

    return offsetParent || getContainingBlock(element) || window;
  }

  function getMainAxisFromPlacement(placement) {
    return ['top', 'bottom'].indexOf(placement) >= 0 ? 'x' : 'y';
  }

  function within(min$1, value, max$1) {
    return max(min$1, min(value, max$1));
  }
  function withinMaxClamp(min, value, max) {
    var v = within(min, value, max);
    return v > max ? max : v;
  }

  function getFreshSideObject() {
    return {
      top: 0,
      right: 0,
      bottom: 0,
      left: 0
    };
  }

  function mergePaddingObject(paddingObject) {
    return Object.assign({}, getFreshSideObject(), paddingObject);
  }

  function expandToHashMap(value, keys) {
    return keys.reduce(function (hashMap, key) {
      hashMap[key] = value;
      return hashMap;
    }, {});
  }

  var toPaddingObject = function toPaddingObject(padding, state) {
    padding = typeof padding === 'function' ? padding(Object.assign({}, state.rects, {
      placement: state.placement
    })) : padding;
    return mergePaddingObject(typeof padding !== 'number' ? padding : expandToHashMap(padding, basePlacements));
  };

  function arrow(_ref) {
    var _state$modifiersData$;

    var state = _ref.state,
        name = _ref.name,
        options = _ref.options;
    var arrowElement = state.elements.arrow;
    var popperOffsets = state.modifiersData.popperOffsets;
    var basePlacement = getBasePlacement(state.placement);
    var axis = getMainAxisFromPlacement(basePlacement);
    var isVertical = [left, right].indexOf(basePlacement) >= 0;
    var len = isVertical ? 'height' : 'width';

    if (!arrowElement || !popperOffsets) {
      return;
    }

    var paddingObject = toPaddingObject(options.padding, state);
    var arrowRect = getLayoutRect(arrowElement);
    var minProp = axis === 'y' ? top : left;
    var maxProp = axis === 'y' ? bottom : right;
    var endDiff = state.rects.reference[len] + state.rects.reference[axis] - popperOffsets[axis] - state.rects.popper[len];
    var startDiff = popperOffsets[axis] - state.rects.reference[axis];
    var arrowOffsetParent = getOffsetParent(arrowElement);
    var clientSize = arrowOffsetParent ? axis === 'y' ? arrowOffsetParent.clientHeight || 0 : arrowOffsetParent.clientWidth || 0 : 0;
    var centerToReference = endDiff / 2 - startDiff / 2; // Make sure the arrow doesn't overflow the popper if the center point is
    // outside of the popper bounds

    var min = paddingObject[minProp];
    var max = clientSize - arrowRect[len] - paddingObject[maxProp];
    var center = clientSize / 2 - arrowRect[len] / 2 + centerToReference;
    var offset = within(min, center, max); // Prevents breaking syntax highlighting...

    var axisProp = axis;
    state.modifiersData[name] = (_state$modifiersData$ = {}, _state$modifiersData$[axisProp] = offset, _state$modifiersData$.centerOffset = offset - center, _state$modifiersData$);
  }

  function effect$1(_ref2) {
    var state = _ref2.state,
        options = _ref2.options;
    var _options$element = options.element,
        arrowElement = _options$element === void 0 ? '[data-popper-arrow]' : _options$element;

    if (arrowElement == null) {
      return;
    } // CSS selector


    if (typeof arrowElement === 'string') {
      arrowElement = state.elements.popper.querySelector(arrowElement);

      if (!arrowElement) {
        return;
      }
    }

    if (!contains(state.elements.popper, arrowElement)) {
      return;
    }

    state.elements.arrow = arrowElement;
  } // eslint-disable-next-line import/no-unused-modules


  const arrow$1 = {
    name: 'arrow',
    enabled: true,
    phase: 'main',
    fn: arrow,
    effect: effect$1,
    requires: ['popperOffsets'],
    requiresIfExists: ['preventOverflow']
  };

  function getVariation(placement) {
    return placement.split('-')[1];
  }

  var unsetSides = {
    top: 'auto',
    right: 'auto',
    bottom: 'auto',
    left: 'auto'
  }; // Round the offsets to the nearest suitable subpixel based on the DPR.
  // Zooming can change the DPR, but it seems to report a value that will
  // cleanly divide the values into the appropriate subpixels.

  function roundOffsetsByDPR(_ref, win) {
    var x = _ref.x,
        y = _ref.y;
    var dpr = win.devicePixelRatio || 1;
    return {
      x: round(x * dpr) / dpr || 0,
      y: round(y * dpr) / dpr || 0
    };
  }

  function mapToStyles(_ref2) {
    var _Object$assign2;

    var popper = _ref2.popper,
        popperRect = _ref2.popperRect,
        placement = _ref2.placement,
        variation = _ref2.variation,
        offsets = _ref2.offsets,
        position = _ref2.position,
        gpuAcceleration = _ref2.gpuAcceleration,
        adaptive = _ref2.adaptive,
        roundOffsets = _ref2.roundOffsets,
        isFixed = _ref2.isFixed;
    var _offsets$x = offsets.x,
        x = _offsets$x === void 0 ? 0 : _offsets$x,
        _offsets$y = offsets.y,
        y = _offsets$y === void 0 ? 0 : _offsets$y;

    var _ref3 = typeof roundOffsets === 'function' ? roundOffsets({
      x: x,
      y: y
    }) : {
      x: x,
      y: y
    };

    x = _ref3.x;
    y = _ref3.y;
    var hasX = offsets.hasOwnProperty('x');
    var hasY = offsets.hasOwnProperty('y');
    var sideX = left;
    var sideY = top;
    var win = window;

    if (adaptive) {
      var offsetParent = getOffsetParent(popper);
      var heightProp = 'clientHeight';
      var widthProp = 'clientWidth';

      if (offsetParent === getWindow(popper)) {
        offsetParent = getDocumentElement(popper);

        if (getComputedStyle$1(offsetParent).position !== 'static' && position === 'absolute') {
          heightProp = 'scrollHeight';
          widthProp = 'scrollWidth';
        }
      } // $FlowFixMe[incompatible-cast]: force type refinement, we compare offsetParent with window above, but Flow doesn't detect it


      offsetParent = offsetParent;

      if (placement === top || (placement === left || placement === right) && variation === end) {
        sideY = bottom;
        var offsetY = isFixed && offsetParent === win && win.visualViewport ? win.visualViewport.height : // $FlowFixMe[prop-missing]
        offsetParent[heightProp];
        y -= offsetY - popperRect.height;
        y *= gpuAcceleration ? 1 : -1;
      }

      if (placement === left || (placement === top || placement === bottom) && variation === end) {
        sideX = right;
        var offsetX = isFixed && offsetParent === win && win.visualViewport ? win.visualViewport.width : // $FlowFixMe[prop-missing]
        offsetParent[widthProp];
        x -= offsetX - popperRect.width;
        x *= gpuAcceleration ? 1 : -1;
      }
    }

    var commonStyles = Object.assign({
      position: position
    }, adaptive && unsetSides);

    var _ref4 = roundOffsets === true ? roundOffsetsByDPR({
      x: x,
      y: y
    }, getWindow(popper)) : {
      x: x,
      y: y
    };

    x = _ref4.x;
    y = _ref4.y;

    if (gpuAcceleration) {
      var _Object$assign;

      return Object.assign({}, commonStyles, (_Object$assign = {}, _Object$assign[sideY] = hasY ? '0' : '', _Object$assign[sideX] = hasX ? '0' : '', _Object$assign.transform = (win.devicePixelRatio || 1) <= 1 ? "translate(" + x + "px, " + y + "px)" : "translate3d(" + x + "px, " + y + "px, 0)", _Object$assign));
    }

    return Object.assign({}, commonStyles, (_Object$assign2 = {}, _Object$assign2[sideY] = hasY ? y + "px" : '', _Object$assign2[sideX] = hasX ? x + "px" : '', _Object$assign2.transform = '', _Object$assign2));
  }

  function computeStyles(_ref5) {
    var state = _ref5.state,
        options = _ref5.options;
    var _options$gpuAccelerat = options.gpuAcceleration,
        gpuAcceleration = _options$gpuAccelerat === void 0 ? true : _options$gpuAccelerat,
        _options$adaptive = options.adaptive,
        adaptive = _options$adaptive === void 0 ? true : _options$adaptive,
        _options$roundOffsets = options.roundOffsets,
        roundOffsets = _options$roundOffsets === void 0 ? true : _options$roundOffsets;
    var commonStyles = {
      placement: getBasePlacement(state.placement),
      variation: getVariation(state.placement),
      popper: state.elements.popper,
      popperRect: state.rects.popper,
      gpuAcceleration: gpuAcceleration,
      isFixed: state.options.strategy === 'fixed'
    };

    if (state.modifiersData.popperOffsets != null) {
      state.styles.popper = Object.assign({}, state.styles.popper, mapToStyles(Object.assign({}, commonStyles, {
        offsets: state.modifiersData.popperOffsets,
        position: state.options.strategy,
        adaptive: adaptive,
        roundOffsets: roundOffsets
      })));
    }

    if (state.modifiersData.arrow != null) {
      state.styles.arrow = Object.assign({}, state.styles.arrow, mapToStyles(Object.assign({}, commonStyles, {
        offsets: state.modifiersData.arrow,
        position: 'absolute',
        adaptive: false,
        roundOffsets: roundOffsets
      })));
    }

    state.attributes.popper = Object.assign({}, state.attributes.popper, {
      'data-popper-placement': state.placement
    });
  } // eslint-disable-next-line import/no-unused-modules


  const computeStyles$1 = {
    name: 'computeStyles',
    enabled: true,
    phase: 'beforeWrite',
    fn: computeStyles,
    data: {}
  };

  var passive = {
    passive: true
  };

  function effect(_ref) {
    var state = _ref.state,
        instance = _ref.instance,
        options = _ref.options;
    var _options$scroll = options.scroll,
        scroll = _options$scroll === void 0 ? true : _options$scroll,
        _options$resize = options.resize,
        resize = _options$resize === void 0 ? true : _options$resize;
    var window = getWindow(state.elements.popper);
    var scrollParents = [].concat(state.scrollParents.reference, state.scrollParents.popper);

    if (scroll) {
      scrollParents.forEach(function (scrollParent) {
        scrollParent.addEventListener('scroll', instance.update, passive);
      });
    }

    if (resize) {
      window.addEventListener('resize', instance.update, passive);
    }

    return function () {
      if (scroll) {
        scrollParents.forEach(function (scrollParent) {
          scrollParent.removeEventListener('scroll', instance.update, passive);
        });
      }

      if (resize) {
        window.removeEventListener('resize', instance.update, passive);
      }
    };
  } // eslint-disable-next-line import/no-unused-modules


  const eventListeners = {
    name: 'eventListeners',
    enabled: true,
    phase: 'write',
    fn: function fn() {},
    effect: effect,
    data: {}
  };

  var hash$1 = {
    left: 'right',
    right: 'left',
    bottom: 'top',
    top: 'bottom'
  };
  function getOppositePlacement(placement) {
    return placement.replace(/left|right|bottom|top/g, function (matched) {
      return hash$1[matched];
    });
  }

  var hash = {
    start: 'end',
    end: 'start'
  };
  function getOppositeVariationPlacement(placement) {
    return placement.replace(/start|end/g, function (matched) {
      return hash[matched];
    });
  }

  function getWindowScroll(node) {
    var win = getWindow(node);
    var scrollLeft = win.pageXOffset;
    var scrollTop = win.pageYOffset;
    return {
      scrollLeft: scrollLeft,
      scrollTop: scrollTop
    };
  }

  function getWindowScrollBarX(element) {
    // If <html> has a CSS width greater than the viewport, then this will be
    // incorrect for RTL.
    // Popper 1 is broken in this case and never had a bug report so let's assume
    // it's not an issue. I don't think anyone ever specifies width on <html>
    // anyway.
    // Browsers where the left scrollbar doesn't cause an issue report `0` for
    // this (e.g. Edge 2019, IE11, Safari)
    return getBoundingClientRect(getDocumentElement(element)).left + getWindowScroll(element).scrollLeft;
  }

  function getViewportRect(element, strategy) {
    var win = getWindow(element);
    var html = getDocumentElement(element);
    var visualViewport = win.visualViewport;
    var width = html.clientWidth;
    var height = html.clientHeight;
    var x = 0;
    var y = 0;

    if (visualViewport) {
      width = visualViewport.width;
      height = visualViewport.height;
      var layoutViewport = isLayoutViewport();

      if (layoutViewport || !layoutViewport && strategy === 'fixed') {
        x = visualViewport.offsetLeft;
        y = visualViewport.offsetTop;
      }
    }

    return {
      width: width,
      height: height,
      x: x + getWindowScrollBarX(element),
      y: y
    };
  }

  // of the `<html>` and `<body>` rect bounds if horizontally scrollable

  function getDocumentRect(element) {
    var _element$ownerDocumen;

    var html = getDocumentElement(element);
    var winScroll = getWindowScroll(element);
    var body = (_element$ownerDocumen = element.ownerDocument) == null ? void 0 : _element$ownerDocumen.body;
    var width = max(html.scrollWidth, html.clientWidth, body ? body.scrollWidth : 0, body ? body.clientWidth : 0);
    var height = max(html.scrollHeight, html.clientHeight, body ? body.scrollHeight : 0, body ? body.clientHeight : 0);
    var x = -winScroll.scrollLeft + getWindowScrollBarX(element);
    var y = -winScroll.scrollTop;

    if (getComputedStyle$1(body || html).direction === 'rtl') {
      x += max(html.clientWidth, body ? body.clientWidth : 0) - width;
    }

    return {
      width: width,
      height: height,
      x: x,
      y: y
    };
  }

  function isScrollParent(element) {
    // Firefox wants us to check `-x` and `-y` variations as well
    var _getComputedStyle = getComputedStyle$1(element),
        overflow = _getComputedStyle.overflow,
        overflowX = _getComputedStyle.overflowX,
        overflowY = _getComputedStyle.overflowY;

    return /auto|scroll|overlay|hidden/.test(overflow + overflowY + overflowX);
  }

  function getScrollParent(node) {
    if (['html', 'body', '#document'].indexOf(getNodeName(node)) >= 0) {
      // $FlowFixMe[incompatible-return]: assume body is always available
      return node.ownerDocument.body;
    }

    if (isHTMLElement(node) && isScrollParent(node)) {
      return node;
    }

    return getScrollParent(getParentNode(node));
  }

  /*
  given a DOM element, return the list of all scroll parents, up the list of ancesors
  until we get to the top window object. This list is what we attach scroll listeners
  to, because if any of these parent elements scroll, we'll need to re-calculate the
  reference element's position.
  */

  function listScrollParents(element, list) {
    var _element$ownerDocumen;

    if (list === void 0) {
      list = [];
    }

    var scrollParent = getScrollParent(element);
    var isBody = scrollParent === ((_element$ownerDocumen = element.ownerDocument) == null ? void 0 : _element$ownerDocumen.body);
    var win = getWindow(scrollParent);
    var target = isBody ? [win].concat(win.visualViewport || [], isScrollParent(scrollParent) ? scrollParent : []) : scrollParent;
    var updatedList = list.concat(target);
    return isBody ? updatedList : // $FlowFixMe[incompatible-call]: isBody tells us target will be an HTMLElement here
    updatedList.concat(listScrollParents(getParentNode(target)));
  }

  function rectToClientRect(rect) {
    return Object.assign({}, rect, {
      left: rect.x,
      top: rect.y,
      right: rect.x + rect.width,
      bottom: rect.y + rect.height
    });
  }

  function getInnerBoundingClientRect(element, strategy) {
    var rect = getBoundingClientRect(element, false, strategy === 'fixed');
    rect.top = rect.top + element.clientTop;
    rect.left = rect.left + element.clientLeft;
    rect.bottom = rect.top + element.clientHeight;
    rect.right = rect.left + element.clientWidth;
    rect.width = element.clientWidth;
    rect.height = element.clientHeight;
    rect.x = rect.left;
    rect.y = rect.top;
    return rect;
  }

  function getClientRectFromMixedType(element, clippingParent, strategy) {
    return clippingParent === viewport ? rectToClientRect(getViewportRect(element, strategy)) : isElement(clippingParent) ? getInnerBoundingClientRect(clippingParent, strategy) : rectToClientRect(getDocumentRect(getDocumentElement(element)));
  } // A "clipping parent" is an overflowable container with the characteristic of
  // clipping (or hiding) overflowing elements with a position different from
  // `initial`


  function getClippingParents(element) {
    var clippingParents = listScrollParents(getParentNode(element));
    var canEscapeClipping = ['absolute', 'fixed'].indexOf(getComputedStyle$1(element).position) >= 0;
    var clipperElement = canEscapeClipping && isHTMLElement(element) ? getOffsetParent(element) : element;

    if (!isElement(clipperElement)) {
      return [];
    } // $FlowFixMe[incompatible-return]: https://github.com/facebook/flow/issues/1414


    return clippingParents.filter(function (clippingParent) {
      return isElement(clippingParent) && contains(clippingParent, clipperElement) && getNodeName(clippingParent) !== 'body';
    });
  } // Gets the maximum area that the element is visible in due to any number of
  // clipping parents


  function getClippingRect(element, boundary, rootBoundary, strategy) {
    var mainClippingParents = boundary === 'clippingParents' ? getClippingParents(element) : [].concat(boundary);
    var clippingParents = [].concat(mainClippingParents, [rootBoundary]);
    var firstClippingParent = clippingParents[0];
    var clippingRect = clippingParents.reduce(function (accRect, clippingParent) {
      var rect = getClientRectFromMixedType(element, clippingParent, strategy);
      accRect.top = max(rect.top, accRect.top);
      accRect.right = min(rect.right, accRect.right);
      accRect.bottom = min(rect.bottom, accRect.bottom);
      accRect.left = max(rect.left, accRect.left);
      return accRect;
    }, getClientRectFromMixedType(element, firstClippingParent, strategy));
    clippingRect.width = clippingRect.right - clippingRect.left;
    clippingRect.height = clippingRect.bottom - clippingRect.top;
    clippingRect.x = clippingRect.left;
    clippingRect.y = clippingRect.top;
    return clippingRect;
  }

  function computeOffsets(_ref) {
    var reference = _ref.reference,
        element = _ref.element,
        placement = _ref.placement;
    var basePlacement = placement ? getBasePlacement(placement) : null;
    var variation = placement ? getVariation(placement) : null;
    var commonX = reference.x + reference.width / 2 - element.width / 2;
    var commonY = reference.y + reference.height / 2 - element.height / 2;
    var offsets;

    switch (basePlacement) {
      case top:
        offsets = {
          x: commonX,
          y: reference.y - element.height
        };
        break;

      case bottom:
        offsets = {
          x: commonX,
          y: reference.y + reference.height
        };
        break;

      case right:
        offsets = {
          x: reference.x + reference.width,
          y: commonY
        };
        break;

      case left:
        offsets = {
          x: reference.x - element.width,
          y: commonY
        };
        break;

      default:
        offsets = {
          x: reference.x,
          y: reference.y
        };
    }

    var mainAxis = basePlacement ? getMainAxisFromPlacement(basePlacement) : null;

    if (mainAxis != null) {
      var len = mainAxis === 'y' ? 'height' : 'width';

      switch (variation) {
        case start:
          offsets[mainAxis] = offsets[mainAxis] - (reference[len] / 2 - element[len] / 2);
          break;

        case end:
          offsets[mainAxis] = offsets[mainAxis] + (reference[len] / 2 - element[len] / 2);
          break;
      }
    }

    return offsets;
  }

  function detectOverflow(state, options) {
    if (options === void 0) {
      options = {};
    }

    var _options = options,
        _options$placement = _options.placement,
        placement = _options$placement === void 0 ? state.placement : _options$placement,
        _options$strategy = _options.strategy,
        strategy = _options$strategy === void 0 ? state.strategy : _options$strategy,
        _options$boundary = _options.boundary,
        boundary = _options$boundary === void 0 ? clippingParents : _options$boundary,
        _options$rootBoundary = _options.rootBoundary,
        rootBoundary = _options$rootBoundary === void 0 ? viewport : _options$rootBoundary,
        _options$elementConte = _options.elementContext,
        elementContext = _options$elementConte === void 0 ? popper : _options$elementConte,
        _options$altBoundary = _options.altBoundary,
        altBoundary = _options$altBoundary === void 0 ? false : _options$altBoundary,
        _options$padding = _options.padding,
        padding = _options$padding === void 0 ? 0 : _options$padding;
    var paddingObject = mergePaddingObject(typeof padding !== 'number' ? padding : expandToHashMap(padding, basePlacements));
    var altContext = elementContext === popper ? reference : popper;
    var popperRect = state.rects.popper;
    var element = state.elements[altBoundary ? altContext : elementContext];
    var clippingClientRect = getClippingRect(isElement(element) ? element : element.contextElement || getDocumentElement(state.elements.popper), boundary, rootBoundary, strategy);
    var referenceClientRect = getBoundingClientRect(state.elements.reference);
    var popperOffsets = computeOffsets({
      reference: referenceClientRect,
      element: popperRect,
      strategy: 'absolute',
      placement: placement
    });
    var popperClientRect = rectToClientRect(Object.assign({}, popperRect, popperOffsets));
    var elementClientRect = elementContext === popper ? popperClientRect : referenceClientRect; // positive = overflowing the clipping rect
    // 0 or negative = within the clipping rect

    var overflowOffsets = {
      top: clippingClientRect.top - elementClientRect.top + paddingObject.top,
      bottom: elementClientRect.bottom - clippingClientRect.bottom + paddingObject.bottom,
      left: clippingClientRect.left - elementClientRect.left + paddingObject.left,
      right: elementClientRect.right - clippingClientRect.right + paddingObject.right
    };
    var offsetData = state.modifiersData.offset; // Offsets can be applied only to the popper element

    if (elementContext === popper && offsetData) {
      var offset = offsetData[placement];
      Object.keys(overflowOffsets).forEach(function (key) {
        var multiply = [right, bottom].indexOf(key) >= 0 ? 1 : -1;
        var axis = [top, bottom].indexOf(key) >= 0 ? 'y' : 'x';
        overflowOffsets[key] += offset[axis] * multiply;
      });
    }

    return overflowOffsets;
  }

  function computeAutoPlacement(state, options) {
    if (options === void 0) {
      options = {};
    }

    var _options = options,
        placement = _options.placement,
        boundary = _options.boundary,
        rootBoundary = _options.rootBoundary,
        padding = _options.padding,
        flipVariations = _options.flipVariations,
        _options$allowedAutoP = _options.allowedAutoPlacements,
        allowedAutoPlacements = _options$allowedAutoP === void 0 ? placements : _options$allowedAutoP;
    var variation = getVariation(placement);
    var placements$1 = variation ? flipVariations ? variationPlacements : variationPlacements.filter(function (placement) {
      return getVariation(placement) === variation;
    }) : basePlacements;
    var allowedPlacements = placements$1.filter(function (placement) {
      return allowedAutoPlacements.indexOf(placement) >= 0;
    });

    if (allowedPlacements.length === 0) {
      allowedPlacements = placements$1;
    } // $FlowFixMe[incompatible-type]: Flow seems to have problems with two array unions...


    var overflows = allowedPlacements.reduce(function (acc, placement) {
      acc[placement] = detectOverflow(state, {
        placement: placement,
        boundary: boundary,
        rootBoundary: rootBoundary,
        padding: padding
      })[getBasePlacement(placement)];
      return acc;
    }, {});
    return Object.keys(overflows).sort(function (a, b) {
      return overflows[a] - overflows[b];
    });
  }

  function getExpandedFallbackPlacements(placement) {
    if (getBasePlacement(placement) === auto) {
      return [];
    }

    var oppositePlacement = getOppositePlacement(placement);
    return [getOppositeVariationPlacement(placement), oppositePlacement, getOppositeVariationPlacement(oppositePlacement)];
  }

  function flip(_ref) {
    var state = _ref.state,
        options = _ref.options,
        name = _ref.name;

    if (state.modifiersData[name]._skip) {
      return;
    }

    var _options$mainAxis = options.mainAxis,
        checkMainAxis = _options$mainAxis === void 0 ? true : _options$mainAxis,
        _options$altAxis = options.altAxis,
        checkAltAxis = _options$altAxis === void 0 ? true : _options$altAxis,
        specifiedFallbackPlacements = options.fallbackPlacements,
        padding = options.padding,
        boundary = options.boundary,
        rootBoundary = options.rootBoundary,
        altBoundary = options.altBoundary,
        _options$flipVariatio = options.flipVariations,
        flipVariations = _options$flipVariatio === void 0 ? true : _options$flipVariatio,
        allowedAutoPlacements = options.allowedAutoPlacements;
    var preferredPlacement = state.options.placement;
    var basePlacement = getBasePlacement(preferredPlacement);
    var isBasePlacement = basePlacement === preferredPlacement;
    var fallbackPlacements = specifiedFallbackPlacements || (isBasePlacement || !flipVariations ? [getOppositePlacement(preferredPlacement)] : getExpandedFallbackPlacements(preferredPlacement));
    var placements = [preferredPlacement].concat(fallbackPlacements).reduce(function (acc, placement) {
      return acc.concat(getBasePlacement(placement) === auto ? computeAutoPlacement(state, {
        placement: placement,
        boundary: boundary,
        rootBoundary: rootBoundary,
        padding: padding,
        flipVariations: flipVariations,
        allowedAutoPlacements: allowedAutoPlacements
      }) : placement);
    }, []);
    var referenceRect = state.rects.reference;
    var popperRect = state.rects.popper;
    var checksMap = new Map();
    var makeFallbackChecks = true;
    var firstFittingPlacement = placements[0];

    for (var i = 0; i < placements.length; i++) {
      var placement = placements[i];

      var _basePlacement = getBasePlacement(placement);

      var isStartVariation = getVariation(placement) === start;
      var isVertical = [top, bottom].indexOf(_basePlacement) >= 0;
      var len = isVertical ? 'width' : 'height';
      var overflow = detectOverflow(state, {
        placement: placement,
        boundary: boundary,
        rootBoundary: rootBoundary,
        altBoundary: altBoundary,
        padding: padding
      });
      var mainVariationSide = isVertical ? isStartVariation ? right : left : isStartVariation ? bottom : top;

      if (referenceRect[len] > popperRect[len]) {
        mainVariationSide = getOppositePlacement(mainVariationSide);
      }

      var altVariationSide = getOppositePlacement(mainVariationSide);
      var checks = [];

      if (checkMainAxis) {
        checks.push(overflow[_basePlacement] <= 0);
      }

      if (checkAltAxis) {
        checks.push(overflow[mainVariationSide] <= 0, overflow[altVariationSide] <= 0);
      }

      if (checks.every(function (check) {
        return check;
      })) {
        firstFittingPlacement = placement;
        makeFallbackChecks = false;
        break;
      }

      checksMap.set(placement, checks);
    }

    if (makeFallbackChecks) {
      // `2` may be desired in some cases – research later
      var numberOfChecks = flipVariations ? 3 : 1;

      var _loop = function _loop(_i) {
        var fittingPlacement = placements.find(function (placement) {
          var checks = checksMap.get(placement);

          if (checks) {
            return checks.slice(0, _i).every(function (check) {
              return check;
            });
          }
        });

        if (fittingPlacement) {
          firstFittingPlacement = fittingPlacement;
          return "break";
        }
      };

      for (var _i = numberOfChecks; _i > 0; _i--) {
        var _ret = _loop(_i);

        if (_ret === "break") break;
      }
    }

    if (state.placement !== firstFittingPlacement) {
      state.modifiersData[name]._skip = true;
      state.placement = firstFittingPlacement;
      state.reset = true;
    }
  } // eslint-disable-next-line import/no-unused-modules


  const flip$1 = {
    name: 'flip',
    enabled: true,
    phase: 'main',
    fn: flip,
    requiresIfExists: ['offset'],
    data: {
      _skip: false
    }
  };

  function getSideOffsets(overflow, rect, preventedOffsets) {
    if (preventedOffsets === void 0) {
      preventedOffsets = {
        x: 0,
        y: 0
      };
    }

    return {
      top: overflow.top - rect.height - preventedOffsets.y,
      right: overflow.right - rect.width + preventedOffsets.x,
      bottom: overflow.bottom - rect.height + preventedOffsets.y,
      left: overflow.left - rect.width - preventedOffsets.x
    };
  }

  function isAnySideFullyClipped(overflow) {
    return [top, right, bottom, left].some(function (side) {
      return overflow[side] >= 0;
    });
  }

  function hide(_ref) {
    var state = _ref.state,
        name = _ref.name;
    var referenceRect = state.rects.reference;
    var popperRect = state.rects.popper;
    var preventedOffsets = state.modifiersData.preventOverflow;
    var referenceOverflow = detectOverflow(state, {
      elementContext: 'reference'
    });
    var popperAltOverflow = detectOverflow(state, {
      altBoundary: true
    });
    var referenceClippingOffsets = getSideOffsets(referenceOverflow, referenceRect);
    var popperEscapeOffsets = getSideOffsets(popperAltOverflow, popperRect, preventedOffsets);
    var isReferenceHidden = isAnySideFullyClipped(referenceClippingOffsets);
    var hasPopperEscaped = isAnySideFullyClipped(popperEscapeOffsets);
    state.modifiersData[name] = {
      referenceClippingOffsets: referenceClippingOffsets,
      popperEscapeOffsets: popperEscapeOffsets,
      isReferenceHidden: isReferenceHidden,
      hasPopperEscaped: hasPopperEscaped
    };
    state.attributes.popper = Object.assign({}, state.attributes.popper, {
      'data-popper-reference-hidden': isReferenceHidden,
      'data-popper-escaped': hasPopperEscaped
    });
  } // eslint-disable-next-line import/no-unused-modules


  const hide$1 = {
    name: 'hide',
    enabled: true,
    phase: 'main',
    requiresIfExists: ['preventOverflow'],
    fn: hide
  };

  function distanceAndSkiddingToXY(placement, rects, offset) {
    var basePlacement = getBasePlacement(placement);
    var invertDistance = [left, top].indexOf(basePlacement) >= 0 ? -1 : 1;

    var _ref = typeof offset === 'function' ? offset(Object.assign({}, rects, {
      placement: placement
    })) : offset,
        skidding = _ref[0],
        distance = _ref[1];

    skidding = skidding || 0;
    distance = (distance || 0) * invertDistance;
    return [left, right].indexOf(basePlacement) >= 0 ? {
      x: distance,
      y: skidding
    } : {
      x: skidding,
      y: distance
    };
  }

  function offset(_ref2) {
    var state = _ref2.state,
        options = _ref2.options,
        name = _ref2.name;
    var _options$offset = options.offset,
        offset = _options$offset === void 0 ? [0, 0] : _options$offset;
    var data = placements.reduce(function (acc, placement) {
      acc[placement] = distanceAndSkiddingToXY(placement, state.rects, offset);
      return acc;
    }, {});
    var _data$state$placement = data[state.placement],
        x = _data$state$placement.x,
        y = _data$state$placement.y;

    if (state.modifiersData.popperOffsets != null) {
      state.modifiersData.popperOffsets.x += x;
      state.modifiersData.popperOffsets.y += y;
    }

    state.modifiersData[name] = data;
  } // eslint-disable-next-line import/no-unused-modules


  const offset$1 = {
    name: 'offset',
    enabled: true,
    phase: 'main',
    requires: ['popperOffsets'],
    fn: offset
  };

  function popperOffsets(_ref) {
    var state = _ref.state,
        name = _ref.name;
    // Offsets are the actual position the popper needs to have to be
    // properly positioned near its reference element
    // This is the most basic placement, and will be adjusted by
    // the modifiers in the next step
    state.modifiersData[name] = computeOffsets({
      reference: state.rects.reference,
      element: state.rects.popper,
      strategy: 'absolute',
      placement: state.placement
    });
  } // eslint-disable-next-line import/no-unused-modules


  const popperOffsets$1 = {
    name: 'popperOffsets',
    enabled: true,
    phase: 'read',
    fn: popperOffsets,
    data: {}
  };

  function getAltAxis(axis) {
    return axis === 'x' ? 'y' : 'x';
  }

  function preventOverflow(_ref) {
    var state = _ref.state,
        options = _ref.options,
        name = _ref.name;
    var _options$mainAxis = options.mainAxis,
        checkMainAxis = _options$mainAxis === void 0 ? true : _options$mainAxis,
        _options$altAxis = options.altAxis,
        checkAltAxis = _options$altAxis === void 0 ? false : _options$altAxis,
        boundary = options.boundary,
        rootBoundary = options.rootBoundary,
        altBoundary = options.altBoundary,
        padding = options.padding,
        _options$tether = options.tether,
        tether = _options$tether === void 0 ? true : _options$tether,
        _options$tetherOffset = options.tetherOffset,
        tetherOffset = _options$tetherOffset === void 0 ? 0 : _options$tetherOffset;
    var overflow = detectOverflow(state, {
      boundary: boundary,
      rootBoundary: rootBoundary,
      padding: padding,
      altBoundary: altBoundary
    });
    var basePlacement = getBasePlacement(state.placement);
    var variation = getVariation(state.placement);
    var isBasePlacement = !variation;
    var mainAxis = getMainAxisFromPlacement(basePlacement);
    var altAxis = getAltAxis(mainAxis);
    var popperOffsets = state.modifiersData.popperOffsets;
    var referenceRect = state.rects.reference;
    var popperRect = state.rects.popper;
    var tetherOffsetValue = typeof tetherOffset === 'function' ? tetherOffset(Object.assign({}, state.rects, {
      placement: state.placement
    })) : tetherOffset;
    var normalizedTetherOffsetValue = typeof tetherOffsetValue === 'number' ? {
      mainAxis: tetherOffsetValue,
      altAxis: tetherOffsetValue
    } : Object.assign({
      mainAxis: 0,
      altAxis: 0
    }, tetherOffsetValue);
    var offsetModifierState = state.modifiersData.offset ? state.modifiersData.offset[state.placement] : null;
    var data = {
      x: 0,
      y: 0
    };

    if (!popperOffsets) {
      return;
    }

    if (checkMainAxis) {
      var _offsetModifierState$;

      var mainSide = mainAxis === 'y' ? top : left;
      var altSide = mainAxis === 'y' ? bottom : right;
      var len = mainAxis === 'y' ? 'height' : 'width';
      var offset = popperOffsets[mainAxis];
      var min$1 = offset + overflow[mainSide];
      var max$1 = offset - overflow[altSide];
      var additive = tether ? -popperRect[len] / 2 : 0;
      var minLen = variation === start ? referenceRect[len] : popperRect[len];
      var maxLen = variation === start ? -popperRect[len] : -referenceRect[len]; // We need to include the arrow in the calculation so the arrow doesn't go
      // outside the reference bounds

      var arrowElement = state.elements.arrow;
      var arrowRect = tether && arrowElement ? getLayoutRect(arrowElement) : {
        width: 0,
        height: 0
      };
      var arrowPaddingObject = state.modifiersData['arrow#persistent'] ? state.modifiersData['arrow#persistent'].padding : getFreshSideObject();
      var arrowPaddingMin = arrowPaddingObject[mainSide];
      var arrowPaddingMax = arrowPaddingObject[altSide]; // If the reference length is smaller than the arrow length, we don't want
      // to include its full size in the calculation. If the reference is small
      // and near the edge of a boundary, the popper can overflow even if the
      // reference is not overflowing as well (e.g. virtual elements with no
      // width or height)

      var arrowLen = within(0, referenceRect[len], arrowRect[len]);
      var minOffset = isBasePlacement ? referenceRect[len] / 2 - additive - arrowLen - arrowPaddingMin - normalizedTetherOffsetValue.mainAxis : minLen - arrowLen - arrowPaddingMin - normalizedTetherOffsetValue.mainAxis;
      var maxOffset = isBasePlacement ? -referenceRect[len] / 2 + additive + arrowLen + arrowPaddingMax + normalizedTetherOffsetValue.mainAxis : maxLen + arrowLen + arrowPaddingMax + normalizedTetherOffsetValue.mainAxis;
      var arrowOffsetParent = state.elements.arrow && getOffsetParent(state.elements.arrow);
      var clientOffset = arrowOffsetParent ? mainAxis === 'y' ? arrowOffsetParent.clientTop || 0 : arrowOffsetParent.clientLeft || 0 : 0;
      var offsetModifierValue = (_offsetModifierState$ = offsetModifierState == null ? void 0 : offsetModifierState[mainAxis]) != null ? _offsetModifierState$ : 0;
      var tetherMin = offset + minOffset - offsetModifierValue - clientOffset;
      var tetherMax = offset + maxOffset - offsetModifierValue;
      var preventedOffset = within(tether ? min(min$1, tetherMin) : min$1, offset, tether ? max(max$1, tetherMax) : max$1);
      popperOffsets[mainAxis] = preventedOffset;
      data[mainAxis] = preventedOffset - offset;
    }

    if (checkAltAxis) {
      var _offsetModifierState$2;

      var _mainSide = mainAxis === 'x' ? top : left;

      var _altSide = mainAxis === 'x' ? bottom : right;

      var _offset = popperOffsets[altAxis];

      var _len = altAxis === 'y' ? 'height' : 'width';

      var _min = _offset + overflow[_mainSide];

      var _max = _offset - overflow[_altSide];

      var isOriginSide = [top, left].indexOf(basePlacement) !== -1;

      var _offsetModifierValue = (_offsetModifierState$2 = offsetModifierState == null ? void 0 : offsetModifierState[altAxis]) != null ? _offsetModifierState$2 : 0;

      var _tetherMin = isOriginSide ? _min : _offset - referenceRect[_len] - popperRect[_len] - _offsetModifierValue + normalizedTetherOffsetValue.altAxis;

      var _tetherMax = isOriginSide ? _offset + referenceRect[_len] + popperRect[_len] - _offsetModifierValue - normalizedTetherOffsetValue.altAxis : _max;

      var _preventedOffset = tether && isOriginSide ? withinMaxClamp(_tetherMin, _offset, _tetherMax) : within(tether ? _tetherMin : _min, _offset, tether ? _tetherMax : _max);

      popperOffsets[altAxis] = _preventedOffset;
      data[altAxis] = _preventedOffset - _offset;
    }

    state.modifiersData[name] = data;
  } // eslint-disable-next-line import/no-unused-modules


  const preventOverflow$1 = {
    name: 'preventOverflow',
    enabled: true,
    phase: 'main',
    fn: preventOverflow,
    requiresIfExists: ['offset']
  };

  function getHTMLElementScroll(element) {
    return {
      scrollLeft: element.scrollLeft,
      scrollTop: element.scrollTop
    };
  }

  function getNodeScroll(node) {
    if (node === getWindow(node) || !isHTMLElement(node)) {
      return getWindowScroll(node);
    } else {
      return getHTMLElementScroll(node);
    }
  }

  function isElementScaled(element) {
    var rect = element.getBoundingClientRect();
    var scaleX = round(rect.width) / element.offsetWidth || 1;
    var scaleY = round(rect.height) / element.offsetHeight || 1;
    return scaleX !== 1 || scaleY !== 1;
  } // Returns the composite rect of an element relative to its offsetParent.
  // Composite means it takes into account transforms as well as layout.


  function getCompositeRect(elementOrVirtualElement, offsetParent, isFixed) {
    if (isFixed === void 0) {
      isFixed = false;
    }

    var isOffsetParentAnElement = isHTMLElement(offsetParent);
    var offsetParentIsScaled = isHTMLElement(offsetParent) && isElementScaled(offsetParent);
    var documentElement = getDocumentElement(offsetParent);
    var rect = getBoundingClientRect(elementOrVirtualElement, offsetParentIsScaled, isFixed);
    var scroll = {
      scrollLeft: 0,
      scrollTop: 0
    };
    var offsets = {
      x: 0,
      y: 0
    };

    if (isOffsetParentAnElement || !isOffsetParentAnElement && !isFixed) {
      if (getNodeName(offsetParent) !== 'body' || // https://github.com/popperjs/popper-core/issues/1078
      isScrollParent(documentElement)) {
        scroll = getNodeScroll(offsetParent);
      }

      if (isHTMLElement(offsetParent)) {
        offsets = getBoundingClientRect(offsetParent, true);
        offsets.x += offsetParent.clientLeft;
        offsets.y += offsetParent.clientTop;
      } else if (documentElement) {
        offsets.x = getWindowScrollBarX(documentElement);
      }
    }

    return {
      x: rect.left + scroll.scrollLeft - offsets.x,
      y: rect.top + scroll.scrollTop - offsets.y,
      width: rect.width,
      height: rect.height
    };
  }

  function order(modifiers) {
    var map = new Map();
    var visited = new Set();
    var result = [];
    modifiers.forEach(function (modifier) {
      map.set(modifier.name, modifier);
    }); // On visiting object, check for its dependencies and visit them recursively

    function sort(modifier) {
      visited.add(modifier.name);
      var requires = [].concat(modifier.requires || [], modifier.requiresIfExists || []);
      requires.forEach(function (dep) {
        if (!visited.has(dep)) {
          var depModifier = map.get(dep);

          if (depModifier) {
            sort(depModifier);
          }
        }
      });
      result.push(modifier);
    }

    modifiers.forEach(function (modifier) {
      if (!visited.has(modifier.name)) {
        // check for visited object
        sort(modifier);
      }
    });
    return result;
  }

  function orderModifiers(modifiers) {
    // order based on dependencies
    var orderedModifiers = order(modifiers); // order based on phase

    return modifierPhases.reduce(function (acc, phase) {
      return acc.concat(orderedModifiers.filter(function (modifier) {
        return modifier.phase === phase;
      }));
    }, []);
  }

  function debounce(fn) {
    var pending;
    return function () {
      if (!pending) {
        pending = new Promise(function (resolve) {
          Promise.resolve().then(function () {
            pending = undefined;
            resolve(fn());
          });
        });
      }

      return pending;
    };
  }

  function mergeByName(modifiers) {
    var merged = modifiers.reduce(function (merged, current) {
      var existing = merged[current.name];
      merged[current.name] = existing ? Object.assign({}, existing, current, {
        options: Object.assign({}, existing.options, current.options),
        data: Object.assign({}, existing.data, current.data)
      }) : current;
      return merged;
    }, {}); // IE11 does not support Object.values

    return Object.keys(merged).map(function (key) {
      return merged[key];
    });
  }

  var DEFAULT_OPTIONS = {
    placement: 'bottom',
    modifiers: [],
    strategy: 'absolute'
  };

  function areValidElements() {
    for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }

    return !args.some(function (element) {
      return !(element && typeof element.getBoundingClientRect === 'function');
    });
  }

  function popperGenerator(generatorOptions) {
    if (generatorOptions === void 0) {
      generatorOptions = {};
    }

    var _generatorOptions = generatorOptions,
        _generatorOptions$def = _generatorOptions.defaultModifiers,
        defaultModifiers = _generatorOptions$def === void 0 ? [] : _generatorOptions$def,
        _generatorOptions$def2 = _generatorOptions.defaultOptions,
        defaultOptions = _generatorOptions$def2 === void 0 ? DEFAULT_OPTIONS : _generatorOptions$def2;
    return function createPopper(reference, popper, options) {
      if (options === void 0) {
        options = defaultOptions;
      }

      var state = {
        placement: 'bottom',
        orderedModifiers: [],
        options: Object.assign({}, DEFAULT_OPTIONS, defaultOptions),
        modifiersData: {},
        elements: {
          reference: reference,
          popper: popper
        },
        attributes: {},
        styles: {}
      };
      var effectCleanupFns = [];
      var isDestroyed = false;
      var instance = {
        state: state,
        setOptions: function setOptions(setOptionsAction) {
          var options = typeof setOptionsAction === 'function' ? setOptionsAction(state.options) : setOptionsAction;
          cleanupModifierEffects();
          state.options = Object.assign({}, defaultOptions, state.options, options);
          state.scrollParents = {
            reference: isElement(reference) ? listScrollParents(reference) : reference.contextElement ? listScrollParents(reference.contextElement) : [],
            popper: listScrollParents(popper)
          }; // Orders the modifiers based on their dependencies and `phase`
          // properties

          var orderedModifiers = orderModifiers(mergeByName([].concat(defaultModifiers, state.options.modifiers))); // Strip out disabled modifiers

          state.orderedModifiers = orderedModifiers.filter(function (m) {
            return m.enabled;
          });
          runModifierEffects();
          return instance.update();
        },
        // Sync update – it will always be executed, even if not necessary. This
        // is useful for low frequency updates where sync behavior simplifies the
        // logic.
        // For high frequency updates (e.g. `resize` and `scroll` events), always
        // prefer the async Popper#update method
        forceUpdate: function forceUpdate() {
          if (isDestroyed) {
            return;
          }

          var _state$elements = state.elements,
              reference = _state$elements.reference,
              popper = _state$elements.popper; // Don't proceed if `reference` or `popper` are not valid elements
          // anymore

          if (!areValidElements(reference, popper)) {
            return;
          } // Store the reference and popper rects to be read by modifiers


          state.rects = {
            reference: getCompositeRect(reference, getOffsetParent(popper), state.options.strategy === 'fixed'),
            popper: getLayoutRect(popper)
          }; // Modifiers have the ability to reset the current update cycle. The
          // most common use case for this is the `flip` modifier changing the
          // placement, which then needs to re-run all the modifiers, because the
          // logic was previously ran for the previous placement and is therefore
          // stale/incorrect

          state.reset = false;
          state.placement = state.options.placement; // On each update cycle, the `modifiersData` property for each modifier
          // is filled with the initial data specified by the modifier. This means
          // it doesn't persist and is fresh on each update.
          // To ensure persistent data, use `${name}#persistent`

          state.orderedModifiers.forEach(function (modifier) {
            return state.modifiersData[modifier.name] = Object.assign({}, modifier.data);
          });

          for (var index = 0; index < state.orderedModifiers.length; index++) {
            if (state.reset === true) {
              state.reset = false;
              index = -1;
              continue;
            }

            var _state$orderedModifie = state.orderedModifiers[index],
                fn = _state$orderedModifie.fn,
                _state$orderedModifie2 = _state$orderedModifie.options,
                _options = _state$orderedModifie2 === void 0 ? {} : _state$orderedModifie2,
                name = _state$orderedModifie.name;

            if (typeof fn === 'function') {
              state = fn({
                state: state,
                options: _options,
                name: name,
                instance: instance
              }) || state;
            }
          }
        },
        // Async and optimistically optimized update – it will not be executed if
        // not necessary (debounced to run at most once-per-tick)
        update: debounce(function () {
          return new Promise(function (resolve) {
            instance.forceUpdate();
            resolve(state);
          });
        }),
        destroy: function destroy() {
          cleanupModifierEffects();
          isDestroyed = true;
        }
      };

      if (!areValidElements(reference, popper)) {
        return instance;
      }

      instance.setOptions(options).then(function (state) {
        if (!isDestroyed && options.onFirstUpdate) {
          options.onFirstUpdate(state);
        }
      }); // Modifiers have the ability to execute arbitrary code before the first
      // update cycle runs. They will be executed in the same order as the update
      // cycle. This is useful when a modifier adds some persistent data that
      // other modifiers need to use, but the modifier is run after the dependent
      // one.

      function runModifierEffects() {
        state.orderedModifiers.forEach(function (_ref) {
          var name = _ref.name,
              _ref$options = _ref.options,
              options = _ref$options === void 0 ? {} : _ref$options,
              effect = _ref.effect;

          if (typeof effect === 'function') {
            var cleanupFn = effect({
              state: state,
              name: name,
              instance: instance,
              options: options
            });

            var noopFn = function noopFn() {};

            effectCleanupFns.push(cleanupFn || noopFn);
          }
        });
      }

      function cleanupModifierEffects() {
        effectCleanupFns.forEach(function (fn) {
          return fn();
        });
        effectCleanupFns = [];
      }

      return instance;
    };
  }
  var createPopper$2 = /*#__PURE__*/popperGenerator(); // eslint-disable-next-line import/no-unused-modules

  var defaultModifiers$1 = [eventListeners, popperOffsets$1, computeStyles$1, applyStyles$1];
  var createPopper$1 = /*#__PURE__*/popperGenerator({
    defaultModifiers: defaultModifiers$1
  }); // eslint-disable-next-line import/no-unused-modules

  var defaultModifiers = [eventListeners, popperOffsets$1, computeStyles$1, applyStyles$1, offset$1, flip$1, preventOverflow$1, arrow$1, hide$1];
  var createPopper = /*#__PURE__*/popperGenerator({
    defaultModifiers: defaultModifiers
  }); // eslint-disable-next-line import/no-unused-modules

  const Popper = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
    __proto__: null,
    afterMain,
    afterRead,
    afterWrite,
    applyStyles: applyStyles$1,
    arrow: arrow$1,
    auto,
    basePlacements,
    beforeMain,
    beforeRead,
    beforeWrite,
    bottom,
    clippingParents,
    computeStyles: computeStyles$1,
    createPopper,
    createPopperBase: createPopper$2,
    createPopperLite: createPopper$1,
    detectOverflow,
    end,
    eventListeners,
    flip: flip$1,
    hide: hide$1,
    left,
    main,
    modifierPhases,
    offset: offset$1,
    placements,
    popper,
    popperGenerator,
    popperOffsets: popperOffsets$1,
    preventOverflow: preventOverflow$1,
    read,
    reference,
    right,
    start,
    top,
    variationPlacements,
    viewport,
    write
  }, Symbol.toStringTag, { value: 'Module' }));

  /**
   * --------------------------------------------------------------------------
   * Bootstrap dropdown.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$a = 'dropdown';
  const DATA_KEY$6 = 'bs.dropdown';
  const EVENT_KEY$6 = `.${DATA_KEY$6}`;
  const DATA_API_KEY$3 = '.data-api';
  const ESCAPE_KEY$2 = 'Escape';
  const TAB_KEY$1 = 'Tab';
  const ARROW_UP_KEY$1 = 'ArrowUp';
  const ARROW_DOWN_KEY$1 = 'ArrowDown';
  const RIGHT_MOUSE_BUTTON = 2; // MouseEvent.button value for the secondary button, usually the right button

  const EVENT_HIDE$5 = `hide${EVENT_KEY$6}`;
  const EVENT_HIDDEN$5 = `hidden${EVENT_KEY$6}`;
  const EVENT_SHOW$5 = `show${EVENT_KEY$6}`;
  const EVENT_SHOWN$5 = `shown${EVENT_KEY$6}`;
  const EVENT_CLICK_DATA_API$3 = `click${EVENT_KEY$6}${DATA_API_KEY$3}`;
  const EVENT_KEYDOWN_DATA_API = `keydown${EVENT_KEY$6}${DATA_API_KEY$3}`;
  const EVENT_KEYUP_DATA_API = `keyup${EVENT_KEY$6}${DATA_API_KEY$3}`;
  const CLASS_NAME_SHOW$6 = 'show';
  const CLASS_NAME_DROPUP = 'dropup';
  const CLASS_NAME_DROPEND = 'dropend';
  const CLASS_NAME_DROPSTART = 'dropstart';
  const CLASS_NAME_DROPUP_CENTER = 'dropup-center';
  const CLASS_NAME_DROPDOWN_CENTER = 'dropdown-center';
  const SELECTOR_DATA_TOGGLE$3 = '[data-bs-toggle="dropdown"]:not(.disabled):not(:disabled)';
  const SELECTOR_DATA_TOGGLE_SHOWN = `${SELECTOR_DATA_TOGGLE$3}.${CLASS_NAME_SHOW$6}`;
  const SELECTOR_MENU = '.dropdown-menu';
  const SELECTOR_NAVBAR = '.navbar';
  const SELECTOR_NAVBAR_NAV = '.navbar-nav';
  const SELECTOR_VISIBLE_ITEMS = '.dropdown-menu .dropdown-item:not(.disabled):not(:disabled)';
  const PLACEMENT_TOP = isRTL() ? 'top-end' : 'top-start';
  const PLACEMENT_TOPEND = isRTL() ? 'top-start' : 'top-end';
  const PLACEMENT_BOTTOM = isRTL() ? 'bottom-end' : 'bottom-start';
  const PLACEMENT_BOTTOMEND = isRTL() ? 'bottom-start' : 'bottom-end';
  const PLACEMENT_RIGHT = isRTL() ? 'left-start' : 'right-start';
  const PLACEMENT_LEFT = isRTL() ? 'right-start' : 'left-start';
  const PLACEMENT_TOPCENTER = 'top';
  const PLACEMENT_BOTTOMCENTER = 'bottom';
  const Default$9 = {
    autoClose: true,
    boundary: 'clippingParents',
    display: 'dynamic',
    offset: [0, 2],
    popperConfig: null,
    reference: 'toggle'
  };
  const DefaultType$9 = {
    autoClose: '(boolean|string)',
    boundary: '(string|element)',
    display: 'string',
    offset: '(array|string|function)',
    popperConfig: '(null|object|function)',
    reference: '(string|element|object)'
  };

  /**
   * Class definition
   */

  class Dropdown extends BaseComponent {
    constructor(element, config) {
      super(element, config);
      this._popper = null;
      this._parent = this._element.parentNode; // dropdown wrapper
      // TODO: v6 revert #37011 & change markup https://getbootstrap.com/docs/5.3/forms/input-group/
      this._menu = SelectorEngine.next(this._element, SELECTOR_MENU)[0] || SelectorEngine.prev(this._element, SELECTOR_MENU)[0] || SelectorEngine.findOne(SELECTOR_MENU, this._parent);
      this._inNavbar = this._detectNavbar();
    }

    // Getters
    static get Default() {
      return Default$9;
    }
    static get DefaultType() {
      return DefaultType$9;
    }
    static get NAME() {
      return NAME$a;
    }

    // Public
    toggle() {
      return this._isShown() ? this.hide() : this.show();
    }
    show() {
      if (isDisabled(this._element) || this._isShown()) {
        return;
      }
      const relatedTarget = {
        relatedTarget: this._element
      };
      const showEvent = EventHandler.trigger(this._element, EVENT_SHOW$5, relatedTarget);
      if (showEvent.defaultPrevented) {
        return;
      }
      this._createPopper();

      // If this is a touch-enabled device we add extra
      // empty mouseover listeners to the body's immediate children;
      // only needed because of broken event delegation on iOS
      // https://www.quirksmode.org/blog/archives/2014/02/mouse_event_bub.html
      if ('ontouchstart' in document.documentElement && !this._parent.closest(SELECTOR_NAVBAR_NAV)) {
        for (const element of [].concat(...document.body.children)) {
          EventHandler.on(element, 'mouseover', noop);
        }
      }
      this._element.focus();
      this._element.setAttribute('aria-expanded', true);
      this._menu.classList.add(CLASS_NAME_SHOW$6);
      this._element.classList.add(CLASS_NAME_SHOW$6);
      EventHandler.trigger(this._element, EVENT_SHOWN$5, relatedTarget);
    }
    hide() {
      if (isDisabled(this._element) || !this._isShown()) {
        return;
      }
      const relatedTarget = {
        relatedTarget: this._element
      };
      this._completeHide(relatedTarget);
    }
    dispose() {
      if (this._popper) {
        this._popper.destroy();
      }
      super.dispose();
    }
    update() {
      this._inNavbar = this._detectNavbar();
      if (this._popper) {
        this._popper.update();
      }
    }

    // Private
    _completeHide(relatedTarget) {
      const hideEvent = EventHandler.trigger(this._element, EVENT_HIDE$5, relatedTarget);
      if (hideEvent.defaultPrevented) {
        return;
      }

      // If this is a touch-enabled device we remove the extra
      // empty mouseover listeners we added for iOS support
      if ('ontouchstart' in document.documentElement) {
        for (const element of [].concat(...document.body.children)) {
          EventHandler.off(element, 'mouseover', noop);
        }
      }
      if (this._popper) {
        this._popper.destroy();
      }
      this._menu.classList.remove(CLASS_NAME_SHOW$6);
      this._element.classList.remove(CLASS_NAME_SHOW$6);
      this._element.setAttribute('aria-expanded', 'false');
      Manipulator.removeDataAttribute(this._menu, 'popper');
      EventHandler.trigger(this._element, EVENT_HIDDEN$5, relatedTarget);
    }
    _getConfig(config) {
      config = super._getConfig(config);
      if (typeof config.reference === 'object' && !isElement$1(config.reference) && typeof config.reference.getBoundingClientRect !== 'function') {
        // Popper virtual elements require a getBoundingClientRect method
        throw new TypeError(`${NAME$a.toUpperCase()}: Option "reference" provided type "object" without a required "getBoundingClientRect" method.`);
      }
      return config;
    }
    _createPopper() {
      if (typeof Popper === 'undefined') {
        throw new TypeError('Bootstrap\'s dropdowns require Popper (https://popper.js.org)');
      }
      let referenceElement = this._element;
      if (this._config.reference === 'parent') {
        referenceElement = this._parent;
      } else if (isElement$1(this._config.reference)) {
        referenceElement = getElement(this._config.reference);
      } else if (typeof this._config.reference === 'object') {
        referenceElement = this._config.reference;
      }
      const popperConfig = this._getPopperConfig();
      this._popper = createPopper(referenceElement, this._menu, popperConfig);
    }
    _isShown() {
      return this._menu.classList.contains(CLASS_NAME_SHOW$6);
    }
    _getPlacement() {
      const parentDropdown = this._parent;
      if (parentDropdown.classList.contains(CLASS_NAME_DROPEND)) {
        return PLACEMENT_RIGHT;
      }
      if (parentDropdown.classList.contains(CLASS_NAME_DROPSTART)) {
        return PLACEMENT_LEFT;
      }
      if (parentDropdown.classList.contains(CLASS_NAME_DROPUP_CENTER)) {
        return PLACEMENT_TOPCENTER;
      }
      if (parentDropdown.classList.contains(CLASS_NAME_DROPDOWN_CENTER)) {
        return PLACEMENT_BOTTOMCENTER;
      }

      // We need to trim the value because custom properties can also include spaces
      const isEnd = getComputedStyle(this._menu).getPropertyValue('--bs-position').trim() === 'end';
      if (parentDropdown.classList.contains(CLASS_NAME_DROPUP)) {
        return isEnd ? PLACEMENT_TOPEND : PLACEMENT_TOP;
      }
      return isEnd ? PLACEMENT_BOTTOMEND : PLACEMENT_BOTTOM;
    }
    _detectNavbar() {
      return this._element.closest(SELECTOR_NAVBAR) !== null;
    }
    _getOffset() {
      const {
        offset
      } = this._config;
      if (typeof offset === 'string') {
        return offset.split(',').map(value => Number.parseInt(value, 10));
      }
      if (typeof offset === 'function') {
        return popperData => offset(popperData, this._element);
      }
      return offset;
    }
    _getPopperConfig() {
      const defaultBsPopperConfig = {
        placement: this._getPlacement(),
        modifiers: [{
          name: 'preventOverflow',
          options: {
            boundary: this._config.boundary
          }
        }, {
          name: 'offset',
          options: {
            offset: this._getOffset()
          }
        }]
      };

      // Disable Popper if we have a static display or Dropdown is in Navbar
      if (this._inNavbar || this._config.display === 'static') {
        Manipulator.setDataAttribute(this._menu, 'popper', 'static'); // TODO: v6 remove
        defaultBsPopperConfig.modifiers = [{
          name: 'applyStyles',
          enabled: false
        }];
      }
      return {
        ...defaultBsPopperConfig,
        ...execute(this._config.popperConfig, [defaultBsPopperConfig])
      };
    }
    _selectMenuItem({
      key,
      target
    }) {
      const items = SelectorEngine.find(SELECTOR_VISIBLE_ITEMS, this._menu).filter(element => isVisible(element));
      if (!items.length) {
        return;
      }

      // if target isn't included in items (e.g. when expanding the dropdown)
      // allow cycling to get the last item in case key equals ARROW_UP_KEY
      getNextActiveElement(items, target, key === ARROW_DOWN_KEY$1, !items.includes(target)).focus();
    }

    // Static
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Dropdown.getOrCreateInstance(this, config);
        if (typeof config !== 'string') {
          return;
        }
        if (typeof data[config] === 'undefined') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config]();
      });
    }
    static clearMenus(event) {
      if (event.button === RIGHT_MOUSE_BUTTON || event.type === 'keyup' && event.key !== TAB_KEY$1) {
        return;
      }
      const openToggles = SelectorEngine.find(SELECTOR_DATA_TOGGLE_SHOWN);
      for (const toggle of openToggles) {
        const context = Dropdown.getInstance(toggle);
        if (!context || context._config.autoClose === false) {
          continue;
        }
        const composedPath = event.composedPath();
        const isMenuTarget = composedPath.includes(context._menu);
        if (composedPath.includes(context._element) || context._config.autoClose === 'inside' && !isMenuTarget || context._config.autoClose === 'outside' && isMenuTarget) {
          continue;
        }

        // Tab navigation through the dropdown menu or events from contained inputs shouldn't close the menu
        if (context._menu.contains(event.target) && (event.type === 'keyup' && event.key === TAB_KEY$1 || /input|select|option|textarea|form/i.test(event.target.tagName))) {
          continue;
        }
        const relatedTarget = {
          relatedTarget: context._element
        };
        if (event.type === 'click') {
          relatedTarget.clickEvent = event;
        }
        context._completeHide(relatedTarget);
      }
    }
    static dataApiKeydownHandler(event) {
      // If not an UP | DOWN | ESCAPE key => not a dropdown command
      // If input/textarea && if key is other than ESCAPE => not a dropdown command

      const isInput = /input|textarea/i.test(event.target.tagName);
      const isEscapeEvent = event.key === ESCAPE_KEY$2;
      const isUpOrDownEvent = [ARROW_UP_KEY$1, ARROW_DOWN_KEY$1].includes(event.key);
      if (!isUpOrDownEvent && !isEscapeEvent) {
        return;
      }
      if (isInput && !isEscapeEvent) {
        return;
      }
      event.preventDefault();

      // TODO: v6 revert #37011 & change markup https://getbootstrap.com/docs/5.3/forms/input-group/
      const getToggleButton = this.matches(SELECTOR_DATA_TOGGLE$3) ? this : SelectorEngine.prev(this, SELECTOR_DATA_TOGGLE$3)[0] || SelectorEngine.next(this, SELECTOR_DATA_TOGGLE$3)[0] || SelectorEngine.findOne(SELECTOR_DATA_TOGGLE$3, event.delegateTarget.parentNode);
      const instance = Dropdown.getOrCreateInstance(getToggleButton);
      if (isUpOrDownEvent) {
        event.stopPropagation();
        instance.show();
        instance._selectMenuItem(event);
        return;
      }
      if (instance._isShown()) {
        // else is escape and we check if it is shown
        event.stopPropagation();
        instance.hide();
        getToggleButton.focus();
      }
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(document, EVENT_KEYDOWN_DATA_API, SELECTOR_DATA_TOGGLE$3, Dropdown.dataApiKeydownHandler);
  EventHandler.on(document, EVENT_KEYDOWN_DATA_API, SELECTOR_MENU, Dropdown.dataApiKeydownHandler);
  EventHandler.on(document, EVENT_CLICK_DATA_API$3, Dropdown.clearMenus);
  EventHandler.on(document, EVENT_KEYUP_DATA_API, Dropdown.clearMenus);
  EventHandler.on(document, EVENT_CLICK_DATA_API$3, SELECTOR_DATA_TOGGLE$3, function (event) {
    event.preventDefault();
    Dropdown.getOrCreateInstance(this).toggle();
  });

  /**
   * jQuery
   */

  defineJQueryPlugin(Dropdown);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/backdrop.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$9 = 'backdrop';
  const CLASS_NAME_FADE$4 = 'fade';
  const CLASS_NAME_SHOW$5 = 'show';
  const EVENT_MOUSEDOWN = `mousedown.bs.${NAME$9}`;
  const Default$8 = {
    className: 'modal-backdrop',
    clickCallback: null,
    isAnimated: false,
    isVisible: true,
    // if false, we use the backdrop helper without adding any element to the dom
    rootElement: 'body' // give the choice to place backdrop under different elements
  };
  const DefaultType$8 = {
    className: 'string',
    clickCallback: '(function|null)',
    isAnimated: 'boolean',
    isVisible: 'boolean',
    rootElement: '(element|string)'
  };

  /**
   * Class definition
   */

  class Backdrop extends Config {
    constructor(config) {
      super();
      this._config = this._getConfig(config);
      this._isAppended = false;
      this._element = null;
    }

    // Getters
    static get Default() {
      return Default$8;
    }
    static get DefaultType() {
      return DefaultType$8;
    }
    static get NAME() {
      return NAME$9;
    }

    // Public
    show(callback) {
      if (!this._config.isVisible) {
        execute(callback);
        return;
      }
      this._append();
      const element = this._getElement();
      if (this._config.isAnimated) {
        reflow(element);
      }
      element.classList.add(CLASS_NAME_SHOW$5);
      this._emulateAnimation(() => {
        execute(callback);
      });
    }
    hide(callback) {
      if (!this._config.isVisible) {
        execute(callback);
        return;
      }
      this._getElement().classList.remove(CLASS_NAME_SHOW$5);
      this._emulateAnimation(() => {
        this.dispose();
        execute(callback);
      });
    }
    dispose() {
      if (!this._isAppended) {
        return;
      }
      EventHandler.off(this._element, EVENT_MOUSEDOWN);
      this._element.remove();
      this._isAppended = false;
    }

    // Private
    _getElement() {
      if (!this._element) {
        const backdrop = document.createElement('div');
        backdrop.className = this._config.className;
        if (this._config.isAnimated) {
          backdrop.classList.add(CLASS_NAME_FADE$4);
        }
        this._element = backdrop;
      }
      return this._element;
    }
    _configAfterMerge(config) {
      // use getElement() with the default "body" to get a fresh Element on each instantiation
      config.rootElement = getElement(config.rootElement);
      return config;
    }
    _append() {
      if (this._isAppended) {
        return;
      }
      const element = this._getElement();
      this._config.rootElement.append(element);
      EventHandler.on(element, EVENT_MOUSEDOWN, () => {
        execute(this._config.clickCallback);
      });
      this._isAppended = true;
    }
    _emulateAnimation(callback) {
      executeAfterTransition(callback, this._getElement(), this._config.isAnimated);
    }
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/focustrap.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$8 = 'focustrap';
  const DATA_KEY$5 = 'bs.focustrap';
  const EVENT_KEY$5 = `.${DATA_KEY$5}`;
  const EVENT_FOCUSIN$2 = `focusin${EVENT_KEY$5}`;
  const EVENT_KEYDOWN_TAB = `keydown.tab${EVENT_KEY$5}`;
  const TAB_KEY = 'Tab';
  const TAB_NAV_FORWARD = 'forward';
  const TAB_NAV_BACKWARD = 'backward';
  const Default$7 = {
    autofocus: true,
    trapElement: null // The element to trap focus inside of
  };
  const DefaultType$7 = {
    autofocus: 'boolean',
    trapElement: 'element'
  };

  /**
   * Class definition
   */

  class FocusTrap extends Config {
    constructor(config) {
      super();
      this._config = this._getConfig(config);
      this._isActive = false;
      this._lastTabNavDirection = null;
    }

    // Getters
    static get Default() {
      return Default$7;
    }
    static get DefaultType() {
      return DefaultType$7;
    }
    static get NAME() {
      return NAME$8;
    }

    // Public
    activate() {
      if (this._isActive) {
        return;
      }
      if (this._config.autofocus) {
        this._config.trapElement.focus();
      }
      EventHandler.off(document, EVENT_KEY$5); // guard against infinite focus loop
      EventHandler.on(document, EVENT_FOCUSIN$2, event => this._handleFocusin(event));
      EventHandler.on(document, EVENT_KEYDOWN_TAB, event => this._handleKeydown(event));
      this._isActive = true;
    }
    deactivate() {
      if (!this._isActive) {
        return;
      }
      this._isActive = false;
      EventHandler.off(document, EVENT_KEY$5);
    }

    // Private
    _handleFocusin(event) {
      const {
        trapElement
      } = this._config;
      if (event.target === document || event.target === trapElement || trapElement.contains(event.target)) {
        return;
      }
      const elements = SelectorEngine.focusableChildren(trapElement);
      if (elements.length === 0) {
        trapElement.focus();
      } else if (this._lastTabNavDirection === TAB_NAV_BACKWARD) {
        elements[elements.length - 1].focus();
      } else {
        elements[0].focus();
      }
    }
    _handleKeydown(event) {
      if (event.key !== TAB_KEY) {
        return;
      }
      this._lastTabNavDirection = event.shiftKey ? TAB_NAV_BACKWARD : TAB_NAV_FORWARD;
    }
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/scrollBar.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const SELECTOR_FIXED_CONTENT = '.fixed-top, .fixed-bottom, .is-fixed, .sticky-top';
  const SELECTOR_STICKY_CONTENT = '.sticky-top';
  const PROPERTY_PADDING = 'padding-right';
  const PROPERTY_MARGIN = 'margin-right';

  /**
   * Class definition
   */

  class ScrollBarHelper {
    constructor() {
      this._element = document.body;
    }

    // Public
    getWidth() {
      // https://developer.mozilla.org/en-US/docs/Web/API/Window/innerWidth#usage_notes
      const documentWidth = document.documentElement.clientWidth;
      return Math.abs(window.innerWidth - documentWidth);
    }
    hide() {
      const width = this.getWidth();
      this._disableOverFlow();
      // give padding to element to balance the hidden scrollbar width
      this._setElementAttributes(this._element, PROPERTY_PADDING, calculatedValue => calculatedValue + width);
      // trick: We adjust positive paddingRight and negative marginRight to sticky-top elements to keep showing fullwidth
      this._setElementAttributes(SELECTOR_FIXED_CONTENT, PROPERTY_PADDING, calculatedValue => calculatedValue + width);
      this._setElementAttributes(SELECTOR_STICKY_CONTENT, PROPERTY_MARGIN, calculatedValue => calculatedValue - width);
    }
    reset() {
      this._resetElementAttributes(this._element, 'overflow');
      this._resetElementAttributes(this._element, PROPERTY_PADDING);
      this._resetElementAttributes(SELECTOR_FIXED_CONTENT, PROPERTY_PADDING);
      this._resetElementAttributes(SELECTOR_STICKY_CONTENT, PROPERTY_MARGIN);
    }
    isOverflowing() {
      return this.getWidth() > 0;
    }

    // Private
    _disableOverFlow() {
      this._saveInitialAttribute(this._element, 'overflow');
      this._element.style.overflow = 'hidden';
    }
    _setElementAttributes(selector, styleProperty, callback) {
      const scrollbarWidth = this.getWidth();
      const manipulationCallBack = element => {
        if (element !== this._element && window.innerWidth > element.clientWidth + scrollbarWidth) {
          return;
        }
        this._saveInitialAttribute(element, styleProperty);
        const calculatedValue = window.getComputedStyle(element).getPropertyValue(styleProperty);
        element.style.setProperty(styleProperty, `${callback(Number.parseFloat(calculatedValue))}px`);
      };
      this._applyManipulationCallback(selector, manipulationCallBack);
    }
    _saveInitialAttribute(element, styleProperty) {
      const actualValue = element.style.getPropertyValue(styleProperty);
      if (actualValue) {
        Manipulator.setDataAttribute(element, styleProperty, actualValue);
      }
    }
    _resetElementAttributes(selector, styleProperty) {
      const manipulationCallBack = element => {
        const value = Manipulator.getDataAttribute(element, styleProperty);
        // We only want to remove the property if the value is `null`; the value can also be zero
        if (value === null) {
          element.style.removeProperty(styleProperty);
          return;
        }
        Manipulator.removeDataAttribute(element, styleProperty);
        element.style.setProperty(styleProperty, value);
      };
      this._applyManipulationCallback(selector, manipulationCallBack);
    }
    _applyManipulationCallback(selector, callBack) {
      if (isElement$1(selector)) {
        callBack(selector);
        return;
      }
      for (const sel of SelectorEngine.find(selector, this._element)) {
        callBack(sel);
      }
    }
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap modal.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$7 = 'modal';
  const DATA_KEY$4 = 'bs.modal';
  const EVENT_KEY$4 = `.${DATA_KEY$4}`;
  const DATA_API_KEY$2 = '.data-api';
  const ESCAPE_KEY$1 = 'Escape';
  const EVENT_HIDE$4 = `hide${EVENT_KEY$4}`;
  const EVENT_HIDE_PREVENTED$1 = `hidePrevented${EVENT_KEY$4}`;
  const EVENT_HIDDEN$4 = `hidden${EVENT_KEY$4}`;
  const EVENT_SHOW$4 = `show${EVENT_KEY$4}`;
  const EVENT_SHOWN$4 = `shown${EVENT_KEY$4}`;
  const EVENT_RESIZE$1 = `resize${EVENT_KEY$4}`;
  const EVENT_CLICK_DISMISS = `click.dismiss${EVENT_KEY$4}`;
  const EVENT_MOUSEDOWN_DISMISS = `mousedown.dismiss${EVENT_KEY$4}`;
  const EVENT_KEYDOWN_DISMISS$1 = `keydown.dismiss${EVENT_KEY$4}`;
  const EVENT_CLICK_DATA_API$2 = `click${EVENT_KEY$4}${DATA_API_KEY$2}`;
  const CLASS_NAME_OPEN = 'modal-open';
  const CLASS_NAME_FADE$3 = 'fade';
  const CLASS_NAME_SHOW$4 = 'show';
  const CLASS_NAME_STATIC = 'modal-static';
  const OPEN_SELECTOR$1 = '.modal.show';
  const SELECTOR_DIALOG = '.modal-dialog';
  const SELECTOR_MODAL_BODY = '.modal-body';
  const SELECTOR_DATA_TOGGLE$2 = '[data-bs-toggle="modal"]';
  const Default$6 = {
    backdrop: true,
    focus: true,
    keyboard: true
  };
  const DefaultType$6 = {
    backdrop: '(boolean|string)',
    focus: 'boolean',
    keyboard: 'boolean'
  };

  /**
   * Class definition
   */

  class Modal extends BaseComponent {
    constructor(element, config) {
      super(element, config);
      this._dialog = SelectorEngine.findOne(SELECTOR_DIALOG, this._element);
      this._backdrop = this._initializeBackDrop();
      this._focustrap = this._initializeFocusTrap();
      this._isShown = false;
      this._isTransitioning = false;
      this._scrollBar = new ScrollBarHelper();
      this._addEventListeners();
    }

    // Getters
    static get Default() {
      return Default$6;
    }
    static get DefaultType() {
      return DefaultType$6;
    }
    static get NAME() {
      return NAME$7;
    }

    // Public
    toggle(relatedTarget) {
      return this._isShown ? this.hide() : this.show(relatedTarget);
    }
    show(relatedTarget) {
      if (this._isShown || this._isTransitioning) {
        return;
      }
      const showEvent = EventHandler.trigger(this._element, EVENT_SHOW$4, {
        relatedTarget
      });
      if (showEvent.defaultPrevented) {
        return;
      }
      this._isShown = true;
      this._isTransitioning = true;
      this._scrollBar.hide();
      document.body.classList.add(CLASS_NAME_OPEN);
      this._adjustDialog();
      this._backdrop.show(() => this._showElement(relatedTarget));
    }
    hide() {
      if (!this._isShown || this._isTransitioning) {
        return;
      }
      const hideEvent = EventHandler.trigger(this._element, EVENT_HIDE$4);
      if (hideEvent.defaultPrevented) {
        return;
      }
      this._isShown = false;
      this._isTransitioning = true;
      this._focustrap.deactivate();
      this._element.classList.remove(CLASS_NAME_SHOW$4);
      this._queueCallback(() => this._hideModal(), this._element, this._isAnimated());
    }
    dispose() {
      EventHandler.off(window, EVENT_KEY$4);
      EventHandler.off(this._dialog, EVENT_KEY$4);
      this._backdrop.dispose();
      this._focustrap.deactivate();
      super.dispose();
    }
    handleUpdate() {
      this._adjustDialog();
    }

    // Private
    _initializeBackDrop() {
      return new Backdrop({
        isVisible: Boolean(this._config.backdrop),
        // 'static' option will be translated to true, and booleans will keep their value,
        isAnimated: this._isAnimated()
      });
    }
    _initializeFocusTrap() {
      return new FocusTrap({
        trapElement: this._element
      });
    }
    _showElement(relatedTarget) {
      // try to append dynamic modal
      if (!document.body.contains(this._element)) {
        document.body.append(this._element);
      }
      this._element.style.display = 'block';
      this._element.removeAttribute('aria-hidden');
      this._element.setAttribute('aria-modal', true);
      this._element.setAttribute('role', 'dialog');
      this._element.scrollTop = 0;
      const modalBody = SelectorEngine.findOne(SELECTOR_MODAL_BODY, this._dialog);
      if (modalBody) {
        modalBody.scrollTop = 0;
      }
      reflow(this._element);
      this._element.classList.add(CLASS_NAME_SHOW$4);
      const transitionComplete = () => {
        if (this._config.focus) {
          this._focustrap.activate();
        }
        this._isTransitioning = false;
        EventHandler.trigger(this._element, EVENT_SHOWN$4, {
          relatedTarget
        });
      };
      this._queueCallback(transitionComplete, this._dialog, this._isAnimated());
    }
    _addEventListeners() {
      EventHandler.on(this._element, EVENT_KEYDOWN_DISMISS$1, event => {
        if (event.key !== ESCAPE_KEY$1) {
          return;
        }
        if (this._config.keyboard) {
          this.hide();
          return;
        }
        this._triggerBackdropTransition();
      });
      EventHandler.on(window, EVENT_RESIZE$1, () => {
        if (this._isShown && !this._isTransitioning) {
          this._adjustDialog();
        }
      });
      EventHandler.on(this._element, EVENT_MOUSEDOWN_DISMISS, event => {
        // a bad trick to segregate clicks that may start inside dialog but end outside, and avoid listen to scrollbar clicks
        EventHandler.one(this._element, EVENT_CLICK_DISMISS, event2 => {
          if (this._element !== event.target || this._element !== event2.target) {
            return;
          }
          if (this._config.backdrop === 'static') {
            this._triggerBackdropTransition();
            return;
          }
          if (this._config.backdrop) {
            this.hide();
          }
        });
      });
    }
    _hideModal() {
      this._element.style.display = 'none';
      this._element.setAttribute('aria-hidden', true);
      this._element.removeAttribute('aria-modal');
      this._element.removeAttribute('role');
      this._isTransitioning = false;
      this._backdrop.hide(() => {
        document.body.classList.remove(CLASS_NAME_OPEN);
        this._resetAdjustments();
        this._scrollBar.reset();
        EventHandler.trigger(this._element, EVENT_HIDDEN$4);
      });
    }
    _isAnimated() {
      return this._element.classList.contains(CLASS_NAME_FADE$3);
    }
    _triggerBackdropTransition() {
      const hideEvent = EventHandler.trigger(this._element, EVENT_HIDE_PREVENTED$1);
      if (hideEvent.defaultPrevented) {
        return;
      }
      const isModalOverflowing = this._element.scrollHeight > document.documentElement.clientHeight;
      const initialOverflowY = this._element.style.overflowY;
      // return if the following background transition hasn't yet completed
      if (initialOverflowY === 'hidden' || this._element.classList.contains(CLASS_NAME_STATIC)) {
        return;
      }
      if (!isModalOverflowing) {
        this._element.style.overflowY = 'hidden';
      }
      this._element.classList.add(CLASS_NAME_STATIC);
      this._queueCallback(() => {
        this._element.classList.remove(CLASS_NAME_STATIC);
        this._queueCallback(() => {
          this._element.style.overflowY = initialOverflowY;
        }, this._dialog);
      }, this._dialog);
      this._element.focus();
    }

    /**
     * The following methods are used to handle overflowing modals
     */

    _adjustDialog() {
      const isModalOverflowing = this._element.scrollHeight > document.documentElement.clientHeight;
      const scrollbarWidth = this._scrollBar.getWidth();
      const isBodyOverflowing = scrollbarWidth > 0;
      if (isBodyOverflowing && !isModalOverflowing) {
        const property = isRTL() ? 'paddingLeft' : 'paddingRight';
        this._element.style[property] = `${scrollbarWidth}px`;
      }
      if (!isBodyOverflowing && isModalOverflowing) {
        const property = isRTL() ? 'paddingRight' : 'paddingLeft';
        this._element.style[property] = `${scrollbarWidth}px`;
      }
    }
    _resetAdjustments() {
      this._element.style.paddingLeft = '';
      this._element.style.paddingRight = '';
    }

    // Static
    static jQueryInterface(config, relatedTarget) {
      return this.each(function () {
        const data = Modal.getOrCreateInstance(this, config);
        if (typeof config !== 'string') {
          return;
        }
        if (typeof data[config] === 'undefined') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config](relatedTarget);
      });
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(document, EVENT_CLICK_DATA_API$2, SELECTOR_DATA_TOGGLE$2, function (event) {
    const target = SelectorEngine.getElementFromSelector(this);
    if (['A', 'AREA'].includes(this.tagName)) {
      event.preventDefault();
    }
    EventHandler.one(target, EVENT_SHOW$4, showEvent => {
      if (showEvent.defaultPrevented) {
        // only register focus restorer if modal will actually get shown
        return;
      }
      EventHandler.one(target, EVENT_HIDDEN$4, () => {
        if (isVisible(this)) {
          this.focus();
        }
      });
    });

    // avoid conflict when clicking modal toggler while another one is open
    const alreadyOpen = SelectorEngine.findOne(OPEN_SELECTOR$1);
    if (alreadyOpen) {
      Modal.getInstance(alreadyOpen).hide();
    }
    const data = Modal.getOrCreateInstance(target);
    data.toggle(this);
  });
  enableDismissTrigger(Modal);

  /**
   * jQuery
   */

  defineJQueryPlugin(Modal);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap offcanvas.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$6 = 'offcanvas';
  const DATA_KEY$3 = 'bs.offcanvas';
  const EVENT_KEY$3 = `.${DATA_KEY$3}`;
  const DATA_API_KEY$1 = '.data-api';
  const EVENT_LOAD_DATA_API$2 = `load${EVENT_KEY$3}${DATA_API_KEY$1}`;
  const ESCAPE_KEY = 'Escape';
  const CLASS_NAME_SHOW$3 = 'show';
  const CLASS_NAME_SHOWING$1 = 'showing';
  const CLASS_NAME_HIDING = 'hiding';
  const CLASS_NAME_BACKDROP = 'offcanvas-backdrop';
  const OPEN_SELECTOR = '.offcanvas.show';
  const EVENT_SHOW$3 = `show${EVENT_KEY$3}`;
  const EVENT_SHOWN$3 = `shown${EVENT_KEY$3}`;
  const EVENT_HIDE$3 = `hide${EVENT_KEY$3}`;
  const EVENT_HIDE_PREVENTED = `hidePrevented${EVENT_KEY$3}`;
  const EVENT_HIDDEN$3 = `hidden${EVENT_KEY$3}`;
  const EVENT_RESIZE = `resize${EVENT_KEY$3}`;
  const EVENT_CLICK_DATA_API$1 = `click${EVENT_KEY$3}${DATA_API_KEY$1}`;
  const EVENT_KEYDOWN_DISMISS = `keydown.dismiss${EVENT_KEY$3}`;
  const SELECTOR_DATA_TOGGLE$1 = '[data-bs-toggle="offcanvas"]';
  const Default$5 = {
    backdrop: true,
    keyboard: true,
    scroll: false
  };
  const DefaultType$5 = {
    backdrop: '(boolean|string)',
    keyboard: 'boolean',
    scroll: 'boolean'
  };

  /**
   * Class definition
   */

  class Offcanvas extends BaseComponent {
    constructor(element, config) {
      super(element, config);
      this._isShown = false;
      this._backdrop = this._initializeBackDrop();
      this._focustrap = this._initializeFocusTrap();
      this._addEventListeners();
    }

    // Getters
    static get Default() {
      return Default$5;
    }
    static get DefaultType() {
      return DefaultType$5;
    }
    static get NAME() {
      return NAME$6;
    }

    // Public
    toggle(relatedTarget) {
      return this._isShown ? this.hide() : this.show(relatedTarget);
    }
    show(relatedTarget) {
      if (this._isShown) {
        return;
      }
      const showEvent = EventHandler.trigger(this._element, EVENT_SHOW$3, {
        relatedTarget
      });
      if (showEvent.defaultPrevented) {
        return;
      }
      this._isShown = true;
      this._backdrop.show();
      if (!this._config.scroll) {
        new ScrollBarHelper().hide();
      }
      this._element.setAttribute('aria-modal', true);
      this._element.setAttribute('role', 'dialog');
      this._element.classList.add(CLASS_NAME_SHOWING$1);
      const completeCallBack = () => {
        if (!this._config.scroll || this._config.backdrop) {
          this._focustrap.activate();
        }
        this._element.classList.add(CLASS_NAME_SHOW$3);
        this._element.classList.remove(CLASS_NAME_SHOWING$1);
        EventHandler.trigger(this._element, EVENT_SHOWN$3, {
          relatedTarget
        });
      };
      this._queueCallback(completeCallBack, this._element, true);
    }
    hide() {
      if (!this._isShown) {
        return;
      }
      const hideEvent = EventHandler.trigger(this._element, EVENT_HIDE$3);
      if (hideEvent.defaultPrevented) {
        return;
      }
      this._focustrap.deactivate();
      this._element.blur();
      this._isShown = false;
      this._element.classList.add(CLASS_NAME_HIDING);
      this._backdrop.hide();
      const completeCallback = () => {
        this._element.classList.remove(CLASS_NAME_SHOW$3, CLASS_NAME_HIDING);
        this._element.removeAttribute('aria-modal');
        this._element.removeAttribute('role');
        if (!this._config.scroll) {
          new ScrollBarHelper().reset();
        }
        EventHandler.trigger(this._element, EVENT_HIDDEN$3);
      };
      this._queueCallback(completeCallback, this._element, true);
    }
    dispose() {
      this._backdrop.dispose();
      this._focustrap.deactivate();
      super.dispose();
    }

    // Private
    _initializeBackDrop() {
      const clickCallback = () => {
        if (this._config.backdrop === 'static') {
          EventHandler.trigger(this._element, EVENT_HIDE_PREVENTED);
          return;
        }
        this.hide();
      };

      // 'static' option will be translated to true, and booleans will keep their value
      const isVisible = Boolean(this._config.backdrop);
      return new Backdrop({
        className: CLASS_NAME_BACKDROP,
        isVisible,
        isAnimated: true,
        rootElement: this._element.parentNode,
        clickCallback: isVisible ? clickCallback : null
      });
    }
    _initializeFocusTrap() {
      return new FocusTrap({
        trapElement: this._element
      });
    }
    _addEventListeners() {
      EventHandler.on(this._element, EVENT_KEYDOWN_DISMISS, event => {
        if (event.key !== ESCAPE_KEY) {
          return;
        }
        if (this._config.keyboard) {
          this.hide();
          return;
        }
        EventHandler.trigger(this._element, EVENT_HIDE_PREVENTED);
      });
    }

    // Static
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Offcanvas.getOrCreateInstance(this, config);
        if (typeof config !== 'string') {
          return;
        }
        if (data[config] === undefined || config.startsWith('_') || config === 'constructor') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config](this);
      });
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(document, EVENT_CLICK_DATA_API$1, SELECTOR_DATA_TOGGLE$1, function (event) {
    const target = SelectorEngine.getElementFromSelector(this);
    if (['A', 'AREA'].includes(this.tagName)) {
      event.preventDefault();
    }
    if (isDisabled(this)) {
      return;
    }
    EventHandler.one(target, EVENT_HIDDEN$3, () => {
      // focus on trigger when it is closed
      if (isVisible(this)) {
        this.focus();
      }
    });

    // avoid conflict when clicking a toggler of an offcanvas, while another is open
    const alreadyOpen = SelectorEngine.findOne(OPEN_SELECTOR);
    if (alreadyOpen && alreadyOpen !== target) {
      Offcanvas.getInstance(alreadyOpen).hide();
    }
    const data = Offcanvas.getOrCreateInstance(target);
    data.toggle(this);
  });
  EventHandler.on(window, EVENT_LOAD_DATA_API$2, () => {
    for (const selector of SelectorEngine.find(OPEN_SELECTOR)) {
      Offcanvas.getOrCreateInstance(selector).show();
    }
  });
  EventHandler.on(window, EVENT_RESIZE, () => {
    for (const element of SelectorEngine.find('[aria-modal][class*=show][class*=offcanvas-]')) {
      if (getComputedStyle(element).position !== 'fixed') {
        Offcanvas.getOrCreateInstance(element).hide();
      }
    }
  });
  enableDismissTrigger(Offcanvas);

  /**
   * jQuery
   */

  defineJQueryPlugin(Offcanvas);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/sanitizer.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */

  // js-docs-start allow-list
  const ARIA_ATTRIBUTE_PATTERN = /^aria-[\w-]*$/i;
  const DefaultAllowlist = {
    // Global attributes allowed on any supplied element below.
    '*': ['class', 'dir', 'id', 'lang', 'role', ARIA_ATTRIBUTE_PATTERN],
    a: ['target', 'href', 'title', 'rel'],
    area: [],
    b: [],
    br: [],
    col: [],
    code: [],
    dd: [],
    div: [],
    dl: [],
    dt: [],
    em: [],
    hr: [],
    h1: [],
    h2: [],
    h3: [],
    h4: [],
    h5: [],
    h6: [],
    i: [],
    img: ['src', 'srcset', 'alt', 'title', 'width', 'height'],
    li: [],
    ol: [],
    p: [],
    pre: [],
    s: [],
    small: [],
    span: [],
    sub: [],
    sup: [],
    strong: [],
    u: [],
    ul: []
  };
  // js-docs-end allow-list

  const uriAttributes = new Set(['background', 'cite', 'href', 'itemtype', 'longdesc', 'poster', 'src', 'xlink:href']);

  /**
   * A pattern that recognizes URLs that are safe wrt. XSS in URL navigation
   * contexts.
   *
   * Shout-out to Angular https://github.com/angular/angular/blob/15.2.8/packages/core/src/sanitization/url_sanitizer.ts#L38
   */
  // eslint-disable-next-line unicorn/better-regex
  const SAFE_URL_PATTERN = /^(?!javascript:)(?:[a-z0-9+.-]+:|[^&:/?#]*(?:[/?#]|$))/i;
  const allowedAttribute = (attribute, allowedAttributeList) => {
    const attributeName = attribute.nodeName.toLowerCase();
    if (allowedAttributeList.includes(attributeName)) {
      if (uriAttributes.has(attributeName)) {
        return Boolean(SAFE_URL_PATTERN.test(attribute.nodeValue));
      }
      return true;
    }

    // Check if a regular expression validates the attribute.
    return allowedAttributeList.filter(attributeRegex => attributeRegex instanceof RegExp).some(regex => regex.test(attributeName));
  };
  function sanitizeHtml(unsafeHtml, allowList, sanitizeFunction) {
    if (!unsafeHtml.length) {
      return unsafeHtml;
    }
    if (sanitizeFunction && typeof sanitizeFunction === 'function') {
      return sanitizeFunction(unsafeHtml);
    }
    const domParser = new window.DOMParser();
    const createdDocument = domParser.parseFromString(unsafeHtml, 'text/html');
    const elements = [].concat(...createdDocument.body.querySelectorAll('*'));
    for (const element of elements) {
      const elementName = element.nodeName.toLowerCase();
      if (!Object.keys(allowList).includes(elementName)) {
        element.remove();
        continue;
      }
      const attributeList = [].concat(...element.attributes);
      const allowedAttributes = [].concat(allowList['*'] || [], allowList[elementName] || []);
      for (const attribute of attributeList) {
        if (!allowedAttribute(attribute, allowedAttributes)) {
          element.removeAttribute(attribute.nodeName);
        }
      }
    }
    return createdDocument.body.innerHTML;
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/template-factory.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$5 = 'TemplateFactory';
  const Default$4 = {
    allowList: DefaultAllowlist,
    content: {},
    // { selector : text ,  selector2 : text2 , }
    extraClass: '',
    html: false,
    sanitize: true,
    sanitizeFn: null,
    template: '<div></div>'
  };
  const DefaultType$4 = {
    allowList: 'object',
    content: 'object',
    extraClass: '(string|function)',
    html: 'boolean',
    sanitize: 'boolean',
    sanitizeFn: '(null|function)',
    template: 'string'
  };
  const DefaultContentType = {
    entry: '(string|element|function|null)',
    selector: '(string|element)'
  };

  /**
   * Class definition
   */

  class TemplateFactory extends Config {
    constructor(config) {
      super();
      this._config = this._getConfig(config);
    }

    // Getters
    static get Default() {
      return Default$4;
    }
    static get DefaultType() {
      return DefaultType$4;
    }
    static get NAME() {
      return NAME$5;
    }

    // Public
    getContent() {
      return Object.values(this._config.content).map(config => this._resolvePossibleFunction(config)).filter(Boolean);
    }
    hasContent() {
      return this.getContent().length > 0;
    }
    changeContent(content) {
      this._checkContent(content);
      this._config.content = {
        ...this._config.content,
        ...content
      };
      return this;
    }
    toHtml() {
      const templateWrapper = document.createElement('div');
      templateWrapper.innerHTML = this._maybeSanitize(this._config.template);
      for (const [selector, text] of Object.entries(this._config.content)) {
        this._setContent(templateWrapper, text, selector);
      }
      const template = templateWrapper.children[0];
      const extraClass = this._resolvePossibleFunction(this._config.extraClass);
      if (extraClass) {
        template.classList.add(...extraClass.split(' '));
      }
      return template;
    }

    // Private
    _typeCheckConfig(config) {
      super._typeCheckConfig(config);
      this._checkContent(config.content);
    }
    _checkContent(arg) {
      for (const [selector, content] of Object.entries(arg)) {
        super._typeCheckConfig({
          selector,
          entry: content
        }, DefaultContentType);
      }
    }
    _setContent(template, content, selector) {
      const templateElement = SelectorEngine.findOne(selector, template);
      if (!templateElement) {
        return;
      }
      content = this._resolvePossibleFunction(content);
      if (!content) {
        templateElement.remove();
        return;
      }
      if (isElement$1(content)) {
        this._putElementInTemplate(getElement(content), templateElement);
        return;
      }
      if (this._config.html) {
        templateElement.innerHTML = this._maybeSanitize(content);
        return;
      }
      templateElement.textContent = content;
    }
    _maybeSanitize(arg) {
      return this._config.sanitize ? sanitizeHtml(arg, this._config.allowList, this._config.sanitizeFn) : arg;
    }
    _resolvePossibleFunction(arg) {
      return execute(arg, [this]);
    }
    _putElementInTemplate(element, templateElement) {
      if (this._config.html) {
        templateElement.innerHTML = '';
        templateElement.append(element);
        return;
      }
      templateElement.textContent = element.textContent;
    }
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap tooltip.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$4 = 'tooltip';
  const DISALLOWED_ATTRIBUTES = new Set(['sanitize', 'allowList', 'sanitizeFn']);
  const CLASS_NAME_FADE$2 = 'fade';
  const CLASS_NAME_MODAL = 'modal';
  const CLASS_NAME_SHOW$2 = 'show';
  const SELECTOR_TOOLTIP_INNER = '.tooltip-inner';
  const SELECTOR_MODAL = `.${CLASS_NAME_MODAL}`;
  const EVENT_MODAL_HIDE = 'hide.bs.modal';
  const TRIGGER_HOVER = 'hover';
  const TRIGGER_FOCUS = 'focus';
  const TRIGGER_CLICK = 'click';
  const TRIGGER_MANUAL = 'manual';
  const EVENT_HIDE$2 = 'hide';
  const EVENT_HIDDEN$2 = 'hidden';
  const EVENT_SHOW$2 = 'show';
  const EVENT_SHOWN$2 = 'shown';
  const EVENT_INSERTED = 'inserted';
  const EVENT_CLICK$1 = 'click';
  const EVENT_FOCUSIN$1 = 'focusin';
  const EVENT_FOCUSOUT$1 = 'focusout';
  const EVENT_MOUSEENTER = 'mouseenter';
  const EVENT_MOUSELEAVE = 'mouseleave';
  const AttachmentMap = {
    AUTO: 'auto',
    TOP: 'top',
    RIGHT: isRTL() ? 'left' : 'right',
    BOTTOM: 'bottom',
    LEFT: isRTL() ? 'right' : 'left'
  };
  const Default$3 = {
    allowList: DefaultAllowlist,
    animation: true,
    boundary: 'clippingParents',
    container: false,
    customClass: '',
    delay: 0,
    fallbackPlacements: ['top', 'right', 'bottom', 'left'],
    html: false,
    offset: [0, 6],
    placement: 'top',
    popperConfig: null,
    sanitize: true,
    sanitizeFn: null,
    selector: false,
    template: '<div class="tooltip" role="tooltip">' + '<div class="tooltip-arrow"></div>' + '<div class="tooltip-inner"></div>' + '</div>',
    title: '',
    trigger: 'hover focus'
  };
  const DefaultType$3 = {
    allowList: 'object',
    animation: 'boolean',
    boundary: '(string|element)',
    container: '(string|element|boolean)',
    customClass: '(string|function)',
    delay: '(number|object)',
    fallbackPlacements: 'array',
    html: 'boolean',
    offset: '(array|string|function)',
    placement: '(string|function)',
    popperConfig: '(null|object|function)',
    sanitize: 'boolean',
    sanitizeFn: '(null|function)',
    selector: '(string|boolean)',
    template: 'string',
    title: '(string|element|function)',
    trigger: 'string'
  };

  /**
   * Class definition
   */

  class Tooltip extends BaseComponent {
    constructor(element, config) {
      if (typeof Popper === 'undefined') {
        throw new TypeError('Bootstrap\'s tooltips require Popper (https://popper.js.org)');
      }
      super(element, config);

      // Private
      this._isEnabled = true;
      this._timeout = 0;
      this._isHovered = null;
      this._activeTrigger = {};
      this._popper = null;
      this._templateFactory = null;
      this._newContent = null;

      // Protected
      this.tip = null;
      this._setListeners();
      if (!this._config.selector) {
        this._fixTitle();
      }
    }

    // Getters
    static get Default() {
      return Default$3;
    }
    static get DefaultType() {
      return DefaultType$3;
    }
    static get NAME() {
      return NAME$4;
    }

    // Public
    enable() {
      this._isEnabled = true;
    }
    disable() {
      this._isEnabled = false;
    }
    toggleEnabled() {
      this._isEnabled = !this._isEnabled;
    }
    toggle() {
      if (!this._isEnabled) {
        return;
      }
      this._activeTrigger.click = !this._activeTrigger.click;
      if (this._isShown()) {
        this._leave();
        return;
      }
      this._enter();
    }
    dispose() {
      clearTimeout(this._timeout);
      EventHandler.off(this._element.closest(SELECTOR_MODAL), EVENT_MODAL_HIDE, this._hideModalHandler);
      if (this._element.getAttribute('data-bs-original-title')) {
        this._element.setAttribute('title', this._element.getAttribute('data-bs-original-title'));
      }
      this._disposePopper();
      super.dispose();
    }
    show() {
      if (this._element.style.display === 'none') {
        throw new Error('Please use show on visible elements');
      }
      if (!(this._isWithContent() && this._isEnabled)) {
        return;
      }
      const showEvent = EventHandler.trigger(this._element, this.constructor.eventName(EVENT_SHOW$2));
      const shadowRoot = findShadowRoot(this._element);
      const isInTheDom = (shadowRoot || this._element.ownerDocument.documentElement).contains(this._element);
      if (showEvent.defaultPrevented || !isInTheDom) {
        return;
      }

      // TODO: v6 remove this or make it optional
      this._disposePopper();
      const tip = this._getTipElement();
      this._element.setAttribute('aria-describedby', tip.getAttribute('id'));
      const {
        container
      } = this._config;
      if (!this._element.ownerDocument.documentElement.contains(this.tip)) {
        container.append(tip);
        EventHandler.trigger(this._element, this.constructor.eventName(EVENT_INSERTED));
      }
      this._popper = this._createPopper(tip);
      tip.classList.add(CLASS_NAME_SHOW$2);

      // If this is a touch-enabled device we add extra
      // empty mouseover listeners to the body's immediate children;
      // only needed because of broken event delegation on iOS
      // https://www.quirksmode.org/blog/archives/2014/02/mouse_event_bub.html
      if ('ontouchstart' in document.documentElement) {
        for (const element of [].concat(...document.body.children)) {
          EventHandler.on(element, 'mouseover', noop);
        }
      }
      const complete = () => {
        EventHandler.trigger(this._element, this.constructor.eventName(EVENT_SHOWN$2));
        if (this._isHovered === false) {
          this._leave();
        }
        this._isHovered = false;
      };
      this._queueCallback(complete, this.tip, this._isAnimated());
    }
    hide() {
      if (!this._isShown()) {
        return;
      }
      const hideEvent = EventHandler.trigger(this._element, this.constructor.eventName(EVENT_HIDE$2));
      if (hideEvent.defaultPrevented) {
        return;
      }
      const tip = this._getTipElement();
      tip.classList.remove(CLASS_NAME_SHOW$2);

      // If this is a touch-enabled device we remove the extra
      // empty mouseover listeners we added for iOS support
      if ('ontouchstart' in document.documentElement) {
        for (const element of [].concat(...document.body.children)) {
          EventHandler.off(element, 'mouseover', noop);
        }
      }
      this._activeTrigger[TRIGGER_CLICK] = false;
      this._activeTrigger[TRIGGER_FOCUS] = false;
      this._activeTrigger[TRIGGER_HOVER] = false;
      this._isHovered = null; // it is a trick to support manual triggering

      const complete = () => {
        if (this._isWithActiveTrigger()) {
          return;
        }
        if (!this._isHovered) {
          this._disposePopper();
        }
        this._element.removeAttribute('aria-describedby');
        EventHandler.trigger(this._element, this.constructor.eventName(EVENT_HIDDEN$2));
      };
      this._queueCallback(complete, this.tip, this._isAnimated());
    }
    update() {
      if (this._popper) {
        this._popper.update();
      }
    }

    // Protected
    _isWithContent() {
      return Boolean(this._getTitle());
    }
    _getTipElement() {
      if (!this.tip) {
        this.tip = this._createTipElement(this._newContent || this._getContentForTemplate());
      }
      return this.tip;
    }
    _createTipElement(content) {
      const tip = this._getTemplateFactory(content).toHtml();

      // TODO: remove this check in v6
      if (!tip) {
        return null;
      }
      tip.classList.remove(CLASS_NAME_FADE$2, CLASS_NAME_SHOW$2);
      // TODO: v6 the following can be achieved with CSS only
      tip.classList.add(`bs-${this.constructor.NAME}-auto`);
      const tipId = getUID(this.constructor.NAME).toString();
      tip.setAttribute('id', tipId);
      if (this._isAnimated()) {
        tip.classList.add(CLASS_NAME_FADE$2);
      }
      return tip;
    }
    setContent(content) {
      this._newContent = content;
      if (this._isShown()) {
        this._disposePopper();
        this.show();
      }
    }
    _getTemplateFactory(content) {
      if (this._templateFactory) {
        this._templateFactory.changeContent(content);
      } else {
        this._templateFactory = new TemplateFactory({
          ...this._config,
          // the `content` var has to be after `this._config`
          // to override config.content in case of popover
          content,
          extraClass: this._resolvePossibleFunction(this._config.customClass)
        });
      }
      return this._templateFactory;
    }
    _getContentForTemplate() {
      return {
        [SELECTOR_TOOLTIP_INNER]: this._getTitle()
      };
    }
    _getTitle() {
      return this._resolvePossibleFunction(this._config.title) || this._element.getAttribute('data-bs-original-title');
    }

    // Private
    _initializeOnDelegatedTarget(event) {
      return this.constructor.getOrCreateInstance(event.delegateTarget, this._getDelegateConfig());
    }
    _isAnimated() {
      return this._config.animation || this.tip && this.tip.classList.contains(CLASS_NAME_FADE$2);
    }
    _isShown() {
      return this.tip && this.tip.classList.contains(CLASS_NAME_SHOW$2);
    }
    _createPopper(tip) {
      const placement = execute(this._config.placement, [this, tip, this._element]);
      const attachment = AttachmentMap[placement.toUpperCase()];
      return createPopper(this._element, tip, this._getPopperConfig(attachment));
    }
    _getOffset() {
      const {
        offset
      } = this._config;
      if (typeof offset === 'string') {
        return offset.split(',').map(value => Number.parseInt(value, 10));
      }
      if (typeof offset === 'function') {
        return popperData => offset(popperData, this._element);
      }
      return offset;
    }
    _resolvePossibleFunction(arg) {
      return execute(arg, [this._element]);
    }
    _getPopperConfig(attachment) {
      const defaultBsPopperConfig = {
        placement: attachment,
        modifiers: [{
          name: 'flip',
          options: {
            fallbackPlacements: this._config.fallbackPlacements
          }
        }, {
          name: 'offset',
          options: {
            offset: this._getOffset()
          }
        }, {
          name: 'preventOverflow',
          options: {
            boundary: this._config.boundary
          }
        }, {
          name: 'arrow',
          options: {
            element: `.${this.constructor.NAME}-arrow`
          }
        }, {
          name: 'preSetPlacement',
          enabled: true,
          phase: 'beforeMain',
          fn: data => {
            // Pre-set Popper's placement attribute in order to read the arrow sizes properly.
            // Otherwise, Popper mixes up the width and height dimensions since the initial arrow style is for top placement
            this._getTipElement().setAttribute('data-popper-placement', data.state.placement);
          }
        }]
      };
      return {
        ...defaultBsPopperConfig,
        ...execute(this._config.popperConfig, [defaultBsPopperConfig])
      };
    }
    _setListeners() {
      const triggers = this._config.trigger.split(' ');
      for (const trigger of triggers) {
        if (trigger === 'click') {
          EventHandler.on(this._element, this.constructor.eventName(EVENT_CLICK$1), this._config.selector, event => {
            const context = this._initializeOnDelegatedTarget(event);
            context.toggle();
          });
        } else if (trigger !== TRIGGER_MANUAL) {
          const eventIn = trigger === TRIGGER_HOVER ? this.constructor.eventName(EVENT_MOUSEENTER) : this.constructor.eventName(EVENT_FOCUSIN$1);
          const eventOut = trigger === TRIGGER_HOVER ? this.constructor.eventName(EVENT_MOUSELEAVE) : this.constructor.eventName(EVENT_FOCUSOUT$1);
          EventHandler.on(this._element, eventIn, this._config.selector, event => {
            const context = this._initializeOnDelegatedTarget(event);
            context._activeTrigger[event.type === 'focusin' ? TRIGGER_FOCUS : TRIGGER_HOVER] = true;
            context._enter();
          });
          EventHandler.on(this._element, eventOut, this._config.selector, event => {
            const context = this._initializeOnDelegatedTarget(event);
            context._activeTrigger[event.type === 'focusout' ? TRIGGER_FOCUS : TRIGGER_HOVER] = context._element.contains(event.relatedTarget);
            context._leave();
          });
        }
      }
      this._hideModalHandler = () => {
        if (this._element) {
          this.hide();
        }
      };
      EventHandler.on(this._element.closest(SELECTOR_MODAL), EVENT_MODAL_HIDE, this._hideModalHandler);
    }
    _fixTitle() {
      const title = this._element.getAttribute('title');
      if (!title) {
        return;
      }
      if (!this._element.getAttribute('aria-label') && !this._element.textContent.trim()) {
        this._element.setAttribute('aria-label', title);
      }
      this._element.setAttribute('data-bs-original-title', title); // DO NOT USE IT. Is only for backwards compatibility
      this._element.removeAttribute('title');
    }
    _enter() {
      if (this._isShown() || this._isHovered) {
        this._isHovered = true;
        return;
      }
      this._isHovered = true;
      this._setTimeout(() => {
        if (this._isHovered) {
          this.show();
        }
      }, this._config.delay.show);
    }
    _leave() {
      if (this._isWithActiveTrigger()) {
        return;
      }
      this._isHovered = false;
      this._setTimeout(() => {
        if (!this._isHovered) {
          this.hide();
        }
      }, this._config.delay.hide);
    }
    _setTimeout(handler, timeout) {
      clearTimeout(this._timeout);
      this._timeout = setTimeout(handler, timeout);
    }
    _isWithActiveTrigger() {
      return Object.values(this._activeTrigger).includes(true);
    }
    _getConfig(config) {
      const dataAttributes = Manipulator.getDataAttributes(this._element);
      for (const dataAttribute of Object.keys(dataAttributes)) {
        if (DISALLOWED_ATTRIBUTES.has(dataAttribute)) {
          delete dataAttributes[dataAttribute];
        }
      }
      config = {
        ...dataAttributes,
        ...(typeof config === 'object' && config ? config : {})
      };
      config = this._mergeConfigObj(config);
      config = this._configAfterMerge(config);
      this._typeCheckConfig(config);
      return config;
    }
    _configAfterMerge(config) {
      config.container = config.container === false ? document.body : getElement(config.container);
      if (typeof config.delay === 'number') {
        config.delay = {
          show: config.delay,
          hide: config.delay
        };
      }
      if (typeof config.title === 'number') {
        config.title = config.title.toString();
      }
      if (typeof config.content === 'number') {
        config.content = config.content.toString();
      }
      return config;
    }
    _getDelegateConfig() {
      const config = {};
      for (const [key, value] of Object.entries(this._config)) {
        if (this.constructor.Default[key] !== value) {
          config[key] = value;
        }
      }
      config.selector = false;
      config.trigger = 'manual';

      // In the future can be replaced with:
      // const keysWithDifferentValues = Object.entries(this._config).filter(entry => this.constructor.Default[entry[0]] !== this._config[entry[0]])
      // `Object.fromEntries(keysWithDifferentValues)`
      return config;
    }
    _disposePopper() {
      if (this._popper) {
        this._popper.destroy();
        this._popper = null;
      }
      if (this.tip) {
        this.tip.remove();
        this.tip = null;
      }
    }

    // Static
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Tooltip.getOrCreateInstance(this, config);
        if (typeof config !== 'string') {
          return;
        }
        if (typeof data[config] === 'undefined') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config]();
      });
    }
  }

  /**
   * jQuery
   */

  defineJQueryPlugin(Tooltip);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap popover.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$3 = 'popover';
  const SELECTOR_TITLE = '.popover-header';
  const SELECTOR_CONTENT = '.popover-body';
  const Default$2 = {
    ...Tooltip.Default,
    content: '',
    offset: [0, 8],
    placement: 'right',
    template: '<div class="popover" role="tooltip">' + '<div class="popover-arrow"></div>' + '<h3 class="popover-header"></h3>' + '<div class="popover-body"></div>' + '</div>',
    trigger: 'click'
  };
  const DefaultType$2 = {
    ...Tooltip.DefaultType,
    content: '(null|string|element|function)'
  };

  /**
   * Class definition
   */

  class Popover extends Tooltip {
    // Getters
    static get Default() {
      return Default$2;
    }
    static get DefaultType() {
      return DefaultType$2;
    }
    static get NAME() {
      return NAME$3;
    }

    // Overrides
    _isWithContent() {
      return this._getTitle() || this._getContent();
    }

    // Private
    _getContentForTemplate() {
      return {
        [SELECTOR_TITLE]: this._getTitle(),
        [SELECTOR_CONTENT]: this._getContent()
      };
    }
    _getContent() {
      return this._resolvePossibleFunction(this._config.content);
    }

    // Static
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Popover.getOrCreateInstance(this, config);
        if (typeof config !== 'string') {
          return;
        }
        if (typeof data[config] === 'undefined') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config]();
      });
    }
  }

  /**
   * jQuery
   */

  defineJQueryPlugin(Popover);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap scrollspy.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$2 = 'scrollspy';
  const DATA_KEY$2 = 'bs.scrollspy';
  const EVENT_KEY$2 = `.${DATA_KEY$2}`;
  const DATA_API_KEY = '.data-api';
  const EVENT_ACTIVATE = `activate${EVENT_KEY$2}`;
  const EVENT_CLICK = `click${EVENT_KEY$2}`;
  const EVENT_LOAD_DATA_API$1 = `load${EVENT_KEY$2}${DATA_API_KEY}`;
  const CLASS_NAME_DROPDOWN_ITEM = 'dropdown-item';
  const CLASS_NAME_ACTIVE$1 = 'active';
  const SELECTOR_DATA_SPY = '[data-bs-spy="scroll"]';
  const SELECTOR_TARGET_LINKS = '[href]';
  const SELECTOR_NAV_LIST_GROUP = '.nav, .list-group';
  const SELECTOR_NAV_LINKS = '.nav-link';
  const SELECTOR_NAV_ITEMS = '.nav-item';
  const SELECTOR_LIST_ITEMS = '.list-group-item';
  const SELECTOR_LINK_ITEMS = `${SELECTOR_NAV_LINKS}, ${SELECTOR_NAV_ITEMS} > ${SELECTOR_NAV_LINKS}, ${SELECTOR_LIST_ITEMS}`;
  const SELECTOR_DROPDOWN = '.dropdown';
  const SELECTOR_DROPDOWN_TOGGLE$1 = '.dropdown-toggle';
  const Default$1 = {
    offset: null,
    // TODO: v6 @deprecated, keep it for backwards compatibility reasons
    rootMargin: '0px 0px -25%',
    smoothScroll: false,
    target: null,
    threshold: [0.1, 0.5, 1]
  };
  const DefaultType$1 = {
    offset: '(number|null)',
    // TODO v6 @deprecated, keep it for backwards compatibility reasons
    rootMargin: 'string',
    smoothScroll: 'boolean',
    target: 'element',
    threshold: 'array'
  };

  /**
   * Class definition
   */

  class ScrollSpy extends BaseComponent {
    constructor(element, config) {
      super(element, config);

      // this._element is the observablesContainer and config.target the menu links wrapper
      this._targetLinks = new Map();
      this._observableSections = new Map();
      this._rootElement = getComputedStyle(this._element).overflowY === 'visible' ? null : this._element;
      this._activeTarget = null;
      this._observer = null;
      this._previousScrollData = {
        visibleEntryTop: 0,
        parentScrollTop: 0
      };
      this.refresh(); // initialize
    }

    // Getters
    static get Default() {
      return Default$1;
    }
    static get DefaultType() {
      return DefaultType$1;
    }
    static get NAME() {
      return NAME$2;
    }

    // Public
    refresh() {
      this._initializeTargetsAndObservables();
      this._maybeEnableSmoothScroll();
      if (this._observer) {
        this._observer.disconnect();
      } else {
        this._observer = this._getNewObserver();
      }
      for (const section of this._observableSections.values()) {
        this._observer.observe(section);
      }
    }
    dispose() {
      this._observer.disconnect();
      super.dispose();
    }

    // Private
    _configAfterMerge(config) {
      // TODO: on v6 target should be given explicitly & remove the {target: 'ss-target'} case
      config.target = getElement(config.target) || document.body;

      // TODO: v6 Only for backwards compatibility reasons. Use rootMargin only
      config.rootMargin = config.offset ? `${config.offset}px 0px -30%` : config.rootMargin;
      if (typeof config.threshold === 'string') {
        config.threshold = config.threshold.split(',').map(value => Number.parseFloat(value));
      }
      return config;
    }
    _maybeEnableSmoothScroll() {
      if (!this._config.smoothScroll) {
        return;
      }

      // unregister any previous listeners
      EventHandler.off(this._config.target, EVENT_CLICK);
      EventHandler.on(this._config.target, EVENT_CLICK, SELECTOR_TARGET_LINKS, event => {
        const observableSection = this._observableSections.get(event.target.hash);
        if (observableSection) {
          event.preventDefault();
          const root = this._rootElement || window;
          const height = observableSection.offsetTop - this._element.offsetTop;
          if (root.scrollTo) {
            root.scrollTo({
              top: height,
              behavior: 'smooth'
            });
            return;
          }

          // Chrome 60 doesn't support `scrollTo`
          root.scrollTop = height;
        }
      });
    }
    _getNewObserver() {
      const options = {
        root: this._rootElement,
        threshold: this._config.threshold,
        rootMargin: this._config.rootMargin
      };
      return new IntersectionObserver(entries => this._observerCallback(entries), options);
    }

    // The logic of selection
    _observerCallback(entries) {
      const targetElement = entry => this._targetLinks.get(`#${entry.target.id}`);
      const activate = entry => {
        this._previousScrollData.visibleEntryTop = entry.target.offsetTop;
        this._process(targetElement(entry));
      };
      const parentScrollTop = (this._rootElement || document.documentElement).scrollTop;
      const userScrollsDown = parentScrollTop >= this._previousScrollData.parentScrollTop;
      this._previousScrollData.parentScrollTop = parentScrollTop;
      for (const entry of entries) {
        if (!entry.isIntersecting) {
          this._activeTarget = null;
          this._clearActiveClass(targetElement(entry));
          continue;
        }
        const entryIsLowerThanPrevious = entry.target.offsetTop >= this._previousScrollData.visibleEntryTop;
        // if we are scrolling down, pick the bigger offsetTop
        if (userScrollsDown && entryIsLowerThanPrevious) {
          activate(entry);
          // if parent isn't scrolled, let's keep the first visible item, breaking the iteration
          if (!parentScrollTop) {
            return;
          }
          continue;
        }

        // if we are scrolling up, pick the smallest offsetTop
        if (!userScrollsDown && !entryIsLowerThanPrevious) {
          activate(entry);
        }
      }
    }
    _initializeTargetsAndObservables() {
      this._targetLinks = new Map();
      this._observableSections = new Map();
      const targetLinks = SelectorEngine.find(SELECTOR_TARGET_LINKS, this._config.target);
      for (const anchor of targetLinks) {
        // ensure that the anchor has an id and is not disabled
        if (!anchor.hash || isDisabled(anchor)) {
          continue;
        }
        const observableSection = SelectorEngine.findOne(decodeURI(anchor.hash), this._element);

        // ensure that the observableSection exists & is visible
        if (isVisible(observableSection)) {
          this._targetLinks.set(decodeURI(anchor.hash), anchor);
          this._observableSections.set(anchor.hash, observableSection);
        }
      }
    }
    _process(target) {
      if (this._activeTarget === target) {
        return;
      }
      this._clearActiveClass(this._config.target);
      this._activeTarget = target;
      target.classList.add(CLASS_NAME_ACTIVE$1);
      this._activateParents(target);
      EventHandler.trigger(this._element, EVENT_ACTIVATE, {
        relatedTarget: target
      });
    }
    _activateParents(target) {
      // Activate dropdown parents
      if (target.classList.contains(CLASS_NAME_DROPDOWN_ITEM)) {
        SelectorEngine.findOne(SELECTOR_DROPDOWN_TOGGLE$1, target.closest(SELECTOR_DROPDOWN)).classList.add(CLASS_NAME_ACTIVE$1);
        return;
      }
      for (const listGroup of SelectorEngine.parents(target, SELECTOR_NAV_LIST_GROUP)) {
        // Set triggered links parents as active
        // With both <ul> and <nav> markup a parent is the previous sibling of any nav ancestor
        for (const item of SelectorEngine.prev(listGroup, SELECTOR_LINK_ITEMS)) {
          item.classList.add(CLASS_NAME_ACTIVE$1);
        }
      }
    }
    _clearActiveClass(parent) {
      parent.classList.remove(CLASS_NAME_ACTIVE$1);
      const activeNodes = SelectorEngine.find(`${SELECTOR_TARGET_LINKS}.${CLASS_NAME_ACTIVE$1}`, parent);
      for (const node of activeNodes) {
        node.classList.remove(CLASS_NAME_ACTIVE$1);
      }
    }

    // Static
    static jQueryInterface(config) {
      return this.each(function () {
        const data = ScrollSpy.getOrCreateInstance(this, config);
        if (typeof config !== 'string') {
          return;
        }
        if (data[config] === undefined || config.startsWith('_') || config === 'constructor') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config]();
      });
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(window, EVENT_LOAD_DATA_API$1, () => {
    for (const spy of SelectorEngine.find(SELECTOR_DATA_SPY)) {
      ScrollSpy.getOrCreateInstance(spy);
    }
  });

  /**
   * jQuery
   */

  defineJQueryPlugin(ScrollSpy);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap tab.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$1 = 'tab';
  const DATA_KEY$1 = 'bs.tab';
  const EVENT_KEY$1 = `.${DATA_KEY$1}`;
  const EVENT_HIDE$1 = `hide${EVENT_KEY$1}`;
  const EVENT_HIDDEN$1 = `hidden${EVENT_KEY$1}`;
  const EVENT_SHOW$1 = `show${EVENT_KEY$1}`;
  const EVENT_SHOWN$1 = `shown${EVENT_KEY$1}`;
  const EVENT_CLICK_DATA_API = `click${EVENT_KEY$1}`;
  const EVENT_KEYDOWN = `keydown${EVENT_KEY$1}`;
  const EVENT_LOAD_DATA_API = `load${EVENT_KEY$1}`;
  const ARROW_LEFT_KEY = 'ArrowLeft';
  const ARROW_RIGHT_KEY = 'ArrowRight';
  const ARROW_UP_KEY = 'ArrowUp';
  const ARROW_DOWN_KEY = 'ArrowDown';
  const HOME_KEY = 'Home';
  const END_KEY = 'End';
  const CLASS_NAME_ACTIVE = 'active';
  const CLASS_NAME_FADE$1 = 'fade';
  const CLASS_NAME_SHOW$1 = 'show';
  const CLASS_DROPDOWN = 'dropdown';
  const SELECTOR_DROPDOWN_TOGGLE = '.dropdown-toggle';
  const SELECTOR_DROPDOWN_MENU = '.dropdown-menu';
  const NOT_SELECTOR_DROPDOWN_TOGGLE = `:not(${SELECTOR_DROPDOWN_TOGGLE})`;
  const SELECTOR_TAB_PANEL = '.list-group, .nav, [role="tablist"]';
  const SELECTOR_OUTER = '.nav-item, .list-group-item';
  const SELECTOR_INNER = `.nav-link${NOT_SELECTOR_DROPDOWN_TOGGLE}, .list-group-item${NOT_SELECTOR_DROPDOWN_TOGGLE}, [role="tab"]${NOT_SELECTOR_DROPDOWN_TOGGLE}`;
  const SELECTOR_DATA_TOGGLE = '[data-bs-toggle="tab"], [data-bs-toggle="pill"], [data-bs-toggle="list"]'; // TODO: could only be `tab` in v6
  const SELECTOR_INNER_ELEM = `${SELECTOR_INNER}, ${SELECTOR_DATA_TOGGLE}`;
  const SELECTOR_DATA_TOGGLE_ACTIVE = `.${CLASS_NAME_ACTIVE}[data-bs-toggle="tab"], .${CLASS_NAME_ACTIVE}[data-bs-toggle="pill"], .${CLASS_NAME_ACTIVE}[data-bs-toggle="list"]`;

  /**
   * Class definition
   */

  class Tab extends BaseComponent {
    constructor(element) {
      super(element);
      this._parent = this._element.closest(SELECTOR_TAB_PANEL);
      if (!this._parent) {
        return;
        // TODO: should throw exception in v6
        // throw new TypeError(`${element.outerHTML} has not a valid parent ${SELECTOR_INNER_ELEM}`)
      }

      // Set up initial aria attributes
      this._setInitialAttributes(this._parent, this._getChildren());
      EventHandler.on(this._element, EVENT_KEYDOWN, event => this._keydown(event));
    }

    // Getters
    static get NAME() {
      return NAME$1;
    }

    // Public
    show() {
      // Shows this elem and deactivate the active sibling if exists
      const innerElem = this._element;
      if (this._elemIsActive(innerElem)) {
        return;
      }

      // Search for active tab on same parent to deactivate it
      const active = this._getActiveElem();
      const hideEvent = active ? EventHandler.trigger(active, EVENT_HIDE$1, {
        relatedTarget: innerElem
      }) : null;
      const showEvent = EventHandler.trigger(innerElem, EVENT_SHOW$1, {
        relatedTarget: active
      });
      if (showEvent.defaultPrevented || hideEvent && hideEvent.defaultPrevented) {
        return;
      }
      this._deactivate(active, innerElem);
      this._activate(innerElem, active);
    }

    // Private
    _activate(element, relatedElem) {
      if (!element) {
        return;
      }
      element.classList.add(CLASS_NAME_ACTIVE);
      this._activate(SelectorEngine.getElementFromSelector(element)); // Search and activate/show the proper section

      const complete = () => {
        if (element.getAttribute('role') !== 'tab') {
          element.classList.add(CLASS_NAME_SHOW$1);
          return;
        }
        element.removeAttribute('tabindex');
        element.setAttribute('aria-selected', true);
        this._toggleDropDown(element, true);
        EventHandler.trigger(element, EVENT_SHOWN$1, {
          relatedTarget: relatedElem
        });
      };
      this._queueCallback(complete, element, element.classList.contains(CLASS_NAME_FADE$1));
    }
    _deactivate(element, relatedElem) {
      if (!element) {
        return;
      }
      element.classList.remove(CLASS_NAME_ACTIVE);
      element.blur();
      this._deactivate(SelectorEngine.getElementFromSelector(element)); // Search and deactivate the shown section too

      const complete = () => {
        if (element.getAttribute('role') !== 'tab') {
          element.classList.remove(CLASS_NAME_SHOW$1);
          return;
        }
        element.setAttribute('aria-selected', false);
        element.setAttribute('tabindex', '-1');
        this._toggleDropDown(element, false);
        EventHandler.trigger(element, EVENT_HIDDEN$1, {
          relatedTarget: relatedElem
        });
      };
      this._queueCallback(complete, element, element.classList.contains(CLASS_NAME_FADE$1));
    }
    _keydown(event) {
      if (![ARROW_LEFT_KEY, ARROW_RIGHT_KEY, ARROW_UP_KEY, ARROW_DOWN_KEY, HOME_KEY, END_KEY].includes(event.key)) {
        return;
      }
      event.stopPropagation(); // stopPropagation/preventDefault both added to support up/down keys without scrolling the page
      event.preventDefault();
      const children = this._getChildren().filter(element => !isDisabled(element));
      let nextActiveElement;
      if ([HOME_KEY, END_KEY].includes(event.key)) {
        nextActiveElement = children[event.key === HOME_KEY ? 0 : children.length - 1];
      } else {
        const isNext = [ARROW_RIGHT_KEY, ARROW_DOWN_KEY].includes(event.key);
        nextActiveElement = getNextActiveElement(children, event.target, isNext, true);
      }
      if (nextActiveElement) {
        nextActiveElement.focus({
          preventScroll: true
        });
        Tab.getOrCreateInstance(nextActiveElement).show();
      }
    }
    _getChildren() {
      // collection of inner elements
      return SelectorEngine.find(SELECTOR_INNER_ELEM, this._parent);
    }
    _getActiveElem() {
      return this._getChildren().find(child => this._elemIsActive(child)) || null;
    }
    _setInitialAttributes(parent, children) {
      this._setAttributeIfNotExists(parent, 'role', 'tablist');
      for (const child of children) {
        this._setInitialAttributesOnChild(child);
      }
    }
    _setInitialAttributesOnChild(child) {
      child = this._getInnerElement(child);
      const isActive = this._elemIsActive(child);
      const outerElem = this._getOuterElement(child);
      child.setAttribute('aria-selected', isActive);
      if (outerElem !== child) {
        this._setAttributeIfNotExists(outerElem, 'role', 'presentation');
      }
      if (!isActive) {
        child.setAttribute('tabindex', '-1');
      }
      this._setAttributeIfNotExists(child, 'role', 'tab');

      // set attributes to the related panel too
      this._setInitialAttributesOnTargetPanel(child);
    }
    _setInitialAttributesOnTargetPanel(child) {
      const target = SelectorEngine.getElementFromSelector(child);
      if (!target) {
        return;
      }
      this._setAttributeIfNotExists(target, 'role', 'tabpanel');
      if (child.id) {
        this._setAttributeIfNotExists(target, 'aria-labelledby', `${child.id}`);
      }
    }
    _toggleDropDown(element, open) {
      const outerElem = this._getOuterElement(element);
      if (!outerElem.classList.contains(CLASS_DROPDOWN)) {
        return;
      }
      const toggle = (selector, className) => {
        const element = SelectorEngine.findOne(selector, outerElem);
        if (element) {
          element.classList.toggle(className, open);
        }
      };
      toggle(SELECTOR_DROPDOWN_TOGGLE, CLASS_NAME_ACTIVE);
      toggle(SELECTOR_DROPDOWN_MENU, CLASS_NAME_SHOW$1);
      outerElem.setAttribute('aria-expanded', open);
    }
    _setAttributeIfNotExists(element, attribute, value) {
      if (!element.hasAttribute(attribute)) {
        element.setAttribute(attribute, value);
      }
    }
    _elemIsActive(elem) {
      return elem.classList.contains(CLASS_NAME_ACTIVE);
    }

    // Try to get the inner element (usually the .nav-link)
    _getInnerElement(elem) {
      return elem.matches(SELECTOR_INNER_ELEM) ? elem : SelectorEngine.findOne(SELECTOR_INNER_ELEM, elem);
    }

    // Try to get the outer element (usually the .nav-item)
    _getOuterElement(elem) {
      return elem.closest(SELECTOR_OUTER) || elem;
    }

    // Static
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Tab.getOrCreateInstance(this);
        if (typeof config !== 'string') {
          return;
        }
        if (data[config] === undefined || config.startsWith('_') || config === 'constructor') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config]();
      });
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(document, EVENT_CLICK_DATA_API, SELECTOR_DATA_TOGGLE, function (event) {
    if (['A', 'AREA'].includes(this.tagName)) {
      event.preventDefault();
    }
    if (isDisabled(this)) {
      return;
    }
    Tab.getOrCreateInstance(this).show();
  });

  /**
   * Initialize on focus
   */
  EventHandler.on(window, EVENT_LOAD_DATA_API, () => {
    for (const element of SelectorEngine.find(SELECTOR_DATA_TOGGLE_ACTIVE)) {
      Tab.getOrCreateInstance(element);
    }
  });
  /**
   * jQuery
   */

  defineJQueryPlugin(Tab);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap toast.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME = 'toast';
  const DATA_KEY = 'bs.toast';
  const EVENT_KEY = `.${DATA_KEY}`;
  const EVENT_MOUSEOVER = `mouseover${EVENT_KEY}`;
  const EVENT_MOUSEOUT = `mouseout${EVENT_KEY}`;
  const EVENT_FOCUSIN = `focusin${EVENT_KEY}`;
  const EVENT_FOCUSOUT = `focusout${EVENT_KEY}`;
  const EVENT_HIDE = `hide${EVENT_KEY}`;
  const EVENT_HIDDEN = `hidden${EVENT_KEY}`;
  const EVENT_SHOW = `show${EVENT_KEY}`;
  const EVENT_SHOWN = `shown${EVENT_KEY}`;
  const CLASS_NAME_FADE = 'fade';
  const CLASS_NAME_HIDE = 'hide'; // @deprecated - kept here only for backwards compatibility
  const CLASS_NAME_SHOW = 'show';
  const CLASS_NAME_SHOWING = 'showing';
  const DefaultType = {
    animation: 'boolean',
    autohide: 'boolean',
    delay: 'number'
  };
  const Default = {
    animation: true,
    autohide: true,
    delay: 5000
  };

  /**
   * Class definition
   */

  class Toast extends BaseComponent {
    constructor(element, config) {
      super(element, config);
      this._timeout = null;
      this._hasMouseInteraction = false;
      this._hasKeyboardInteraction = false;
      this._setListeners();
    }

    // Getters
    static get Default() {
      return Default;
    }
    static get DefaultType() {
      return DefaultType;
    }
    static get NAME() {
      return NAME;
    }

    // Public
    show() {
      const showEvent = EventHandler.trigger(this._element, EVENT_SHOW);
      if (showEvent.defaultPrevented) {
        return;
      }
      this._clearTimeout();
      if (this._config.animation) {
        this._element.classList.add(CLASS_NAME_FADE);
      }
      const complete = () => {
        this._element.classList.remove(CLASS_NAME_SHOWING);
        EventHandler.trigger(this._element, EVENT_SHOWN);
        this._maybeScheduleHide();
      };
      this._element.classList.remove(CLASS_NAME_HIDE); // @deprecated
      reflow(this._element);
      this._element.classList.add(CLASS_NAME_SHOW, CLASS_NAME_SHOWING);
      this._queueCallback(complete, this._element, this._config.animation);
    }
    hide() {
      if (!this.isShown()) {
        return;
      }
      const hideEvent = EventHandler.trigger(this._element, EVENT_HIDE);
      if (hideEvent.defaultPrevented) {
        return;
      }
      const complete = () => {
        this._element.classList.add(CLASS_NAME_HIDE); // @deprecated
        this._element.classList.remove(CLASS_NAME_SHOWING, CLASS_NAME_SHOW);
        EventHandler.trigger(this._element, EVENT_HIDDEN);
      };
      this._element.classList.add(CLASS_NAME_SHOWING);
      this._queueCallback(complete, this._element, this._config.animation);
    }
    dispose() {
      this._clearTimeout();
      if (this.isShown()) {
        this._element.classList.remove(CLASS_NAME_SHOW);
      }
      super.dispose();
    }
    isShown() {
      return this._element.classList.contains(CLASS_NAME_SHOW);
    }

    // Private

    _maybeScheduleHide() {
      if (!this._config.autohide) {
        return;
      }
      if (this._hasMouseInteraction || this._hasKeyboardInteraction) {
        return;
      }
      this._timeout = setTimeout(() => {
        this.hide();
      }, this._config.delay);
    }
    _onInteraction(event, isInteracting) {
      switch (event.type) {
        case 'mouseover':
        case 'mouseout':
          {
            this._hasMouseInteraction = isInteracting;
            break;
          }
        case 'focusin':
        case 'focusout':
          {
            this._hasKeyboardInteraction = isInteracting;
            break;
          }
      }
      if (isInteracting) {
        this._clearTimeout();
        return;
      }
      const nextElement = event.relatedTarget;
      if (this._element === nextElement || this._element.contains(nextElement)) {
        return;
      }
      this._maybeScheduleHide();
    }
    _setListeners() {
      EventHandler.on(this._element, EVENT_MOUSEOVER, event => this._onInteraction(event, true));
      EventHandler.on(this._element, EVENT_MOUSEOUT, event => this._onInteraction(event, false));
      EventHandler.on(this._element, EVENT_FOCUSIN, event => this._onInteraction(event, true));
      EventHandler.on(this._element, EVENT_FOCUSOUT, event => this._onInteraction(event, false));
    }
    _clearTimeout() {
      clearTimeout(this._timeout);
      this._timeout = null;
    }

    // Static
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Toast.getOrCreateInstance(this, config);
        if (typeof config === 'string') {
          if (typeof data[config] === 'undefined') {
            throw new TypeError(`No method named "${config}"`);
          }
          data[config](this);
        }
      });
    }
  }

  /**
   * Data API implementation
   */

  enableDismissTrigger(Toast);

  /**
   * jQuery
   */

  defineJQueryPlugin(Toast);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap index.umd.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */

  const index_umd = {
    Alert,
    Button,
    Carousel,
    Collapse,
    Dropdown,
    Modal,
    Offcanvas,
    Popover,
    ScrollSpy,
    Tab,
    Toast,
    Tooltip
  };

  return index_umd;

}));
//# sourceMappingURL=bootstrap.bundle.js.map

;
/**!
 * FlexSearch.js v0.7.41 (Bundle)
 * Author and Copyright: Thomas Wilkerling
 * Licence: Apache-2.0
 * Hosted by Nextapps GmbH
 * https://github.com/nextapps-de/flexsearch
 */
(function _f(self){'use strict';try{if(module)self=module}catch(e){}self._factory=_f;var t;function u(a){return"undefined"!==typeof a?a:!0}function v(a){const b=Array(a);for(let c=0;c<a;c++)b[c]=x();return b}function x(){return Object.create(null)}function aa(a,b){return b.length-a.length}function C(a){return"string"===typeof a}function D(a){return"object"===typeof a}function E(a){return"function"===typeof a};function ba(a,b){var c=ca;if(a&&(b&&(a=F(a,b)),this.H&&(a=F(a,this.H)),this.J&&1<a.length&&(a=F(a,this.J)),c||""===c)){b=a.split(c);if(this.filter){a=this.filter;c=b.length;const d=[];for(let e=0,f=0;e<c;e++){const h=b[e];h&&!a[h]&&(d[f++]=h)}a=d}else a=b;return a}return a}const ca=/[\p{Z}\p{S}\p{P}\p{C}]+/u,da=/[\u0300-\u036f]/g;
function ea(a,b){const c=Object.keys(a),d=c.length,e=[];let f="",h=0;for(let g=0,k,m;g<d;g++)k=c[g],(m=a[k])?(e[h++]=G(b?"(?!\\b)"+k+"(\\b|_)":k),e[h++]=m):f+=(f?"|":"")+k;f&&(e[h++]=G(b?"(?!\\b)("+f+")(\\b|_)":"("+f+")"),e[h]="");return e}function F(a,b){for(let c=0,d=b.length;c<d&&(a=a.replace(b[c],b[c+1]),a);c+=2);return a}function G(a){return new RegExp(a,"g")}function fa(a){let b="",c="";for(let d=0,e=a.length,f;d<e;d++)(f=a[d])!==c&&(b+=c=f);return b};var ia={encode:ha,F:!1,G:""};function ha(a){return ba.call(this,(""+a).toLowerCase(),!1)};const ja={},I={};function ka(a){J(a,"add");J(a,"append");J(a,"search");J(a,"update");J(a,"remove")}function J(a,b){a[b+"Async"]=function(){const c=this,d=arguments;var e=d[d.length-1];let f;E(e)&&(f=e,delete d[d.length-1]);e=new Promise(function(h){setTimeout(function(){c.async=!0;const g=c[b].apply(c,d);c.async=!1;h(g)})});return f?(e.then(f),this):e}};function la(a,b,c,d){const e=a.length;let f=[],h,g,k=0;d&&(d=[]);for(let m=e-1;0<=m;m--){const n=a[m],w=n.length,q=x();let r=!h;for(let l=0;l<w;l++){const p=n[l],A=p.length;if(A)for(let B=0,z,y;B<A;B++)if(y=p[B],h){if(h[y]){if(!m)if(c)c--;else if(f[k++]=y,k===b)return f;if(m||d)q[y]=1;r=!0}if(d&&(z=(g[y]||0)+1,g[y]=z,z<e)){const H=d[z-2]||(d[z-2]=[]);H[H.length]=y}}else q[y]=1}if(d)h||(g=q);else if(!r)return[];h=q}if(d)for(let m=d.length-1,n,w;0<=m;m--){n=d[m];w=n.length;for(let q=0,r;q<w;q++)if(r=
n[q],!h[r]){if(c)c--;else if(f[k++]=r,k===b)return f;h[r]=1}}return f}function ma(a,b){const c=x(),d=x(),e=[];for(let f=0;f<a.length;f++)c[a[f]]=1;for(let f=0,h;f<b.length;f++){h=b[f];for(let g=0,k;g<h.length;g++)k=h[g],c[k]&&!d[k]&&(d[k]=1,e[e.length]=k)}return e};function K(a){this.l=!0!==a&&a;this.cache=x();this.h=[]}function na(a,b,c){D(a)&&(a=a.query);let d=this.cache.get(a);d||(d=this.search(a,b,c),this.cache.set(a,d));return d}K.prototype.set=function(a,b){if(!this.cache[a]){var c=this.h.length;c===this.l?delete this.cache[this.h[c-1]]:c++;for(--c;0<c;c--)this.h[c]=this.h[c-1];this.h[0]=a}this.cache[a]=b};K.prototype.get=function(a){const b=this.cache[a];if(this.l&&b&&(a=this.h.indexOf(a))){const c=this.h[a-1];this.h[a-1]=this.h[a];this.h[a]=c}return b};const pa={memory:{charset:"latin:extra",D:3,B:4,m:!1},performance:{D:3,B:3,s:!1,context:{depth:2,D:1}},match:{charset:"latin:extra",G:"reverse"},score:{charset:"latin:advanced",D:20,B:3,context:{depth:3,D:9}},"default":{}};function qa(a,b,c,d,e,f,h,g){setTimeout(function(){const k=a(c?c+"."+d:d,JSON.stringify(h));k&&k.then?k.then(function(){b.export(a,b,c,e,f+1,g)}):b.export(a,b,c,e,f+1,g)})};function L(a,b){if(!(this instanceof L))return new L(a);var c;if(a){C(a)?a=pa[a]:(c=a.preset)&&(a=Object.assign({},c[c],a));c=a.charset;var d=a.lang;C(c)&&(-1===c.indexOf(":")&&(c+=":default"),c=I[c]);C(d)&&(d=ja[d])}else a={};let e,f,h=a.context||{};this.encode=a.encode||c&&c.encode||ha;this.register=b||x();this.D=e=a.resolution||9;this.G=b=c&&c.G||a.tokenize||"strict";this.depth="strict"===b&&h.depth;this.l=u(h.bidirectional);this.s=f=u(a.optimize);this.m=u(a.fastupdate);this.B=a.minlength||1;this.C=
a.boost;this.map=f?v(e):x();this.A=e=h.resolution||1;this.h=f?v(e):x();this.F=c&&c.F||a.rtl;this.H=(b=a.matcher||d&&d.H)&&ea(b,!1);this.J=(b=a.stemmer||d&&d.J)&&ea(b,!0);if(c=b=a.filter||d&&d.filter){c=b;d=x();for(let g=0,k=c.length;g<k;g++)d[c[g]]=1;c=d}this.filter=c;this.cache=(b=a.cache)&&new K(b)}t=L.prototype;t.append=function(a,b){return this.add(a,b,!0)};
t.add=function(a,b,c,d){if(b&&(a||0===a)){if(!d&&!c&&this.register[a])return this.update(a,b);b=this.encode(b);if(d=b.length){const m=x(),n=x(),w=this.depth,q=this.D;for(let r=0;r<d;r++){let l=b[this.F?d-1-r:r];var e=l.length;if(l&&e>=this.B&&(w||!n[l])){var f=M(q,d,r),h="";switch(this.G){case "full":if(2<e){for(f=0;f<e;f++)for(var g=e;g>f;g--)if(g-f>=this.B){var k=M(q,d,r,e,f);h=l.substring(f,g);N(this,n,h,k,a,c)}break}case "reverse":if(1<e){for(g=e-1;0<g;g--)h=l[g]+h,h.length>=this.B&&N(this,n,
h,M(q,d,r,e,g),a,c);h=""}case "forward":if(1<e){for(g=0;g<e;g++)h+=l[g],h.length>=this.B&&N(this,n,h,f,a,c);break}default:if(this.C&&(f=Math.min(f/this.C(b,l,r)|0,q-1)),N(this,n,l,f,a,c),w&&1<d&&r<d-1)for(e=x(),h=this.A,f=l,g=Math.min(w+1,d-r),e[f]=1,k=1;k<g;k++)if((l=b[this.F?d-1-r-k:r+k])&&l.length>=this.B&&!e[l]){e[l]=1;const p=this.l&&l>f;N(this,m,p?f:l,M(h+(d/2>h?0:1),d,r,g-1,k-1),a,c,p?l:f)}}}}this.m||(this.register[a]=1)}}return this};
function M(a,b,c,d,e){return c&&1<a?b+(d||0)<=a?c+(e||0):(a-1)/(b+(d||0))*(c+(e||0))+1|0:0}function N(a,b,c,d,e,f,h){let g=h?a.h:a.map;if(!b[c]||h&&!b[c][h])a.s&&(g=g[d]),h?(b=b[c]||(b[c]=x()),b[h]=1,g=g[h]||(g[h]=x())):b[c]=1,g=g[c]||(g[c]=[]),a.s||(g=g[d]||(g[d]=[])),f&&g.includes(e)||(g[g.length]=e,a.m&&(a=a.register[e]||(a.register[e]=[]),a[a.length]=g))}
t.search=function(a,b,c){c||(!b&&D(a)?(c=a,a=c.query):D(b)&&(c=b));let d=[],e;let f,h=0;if(c){a=c.query||a;b=c.limit;h=c.offset||0;var g=c.context;f=c.suggest}if(a&&(a=this.encode(""+a),e=a.length,1<e)){c=x();var k=[];for(let n=0,w=0,q;n<e;n++)if((q=a[n])&&q.length>=this.B&&!c[q])if(this.s||f||this.map[q])k[w++]=q,c[q]=1;else return d;a=k;e=a.length}if(!e)return d;b||(b=100);g=this.depth&&1<e&&!1!==g;c=0;let m;g?(m=a[0],c=1):1<e&&a.sort(aa);for(let n,w;c<e;c++){w=a[c];g?(n=ra(this,d,f,b,h,2===e,w,
m),f&&!1===n&&d.length||(m=w)):n=ra(this,d,f,b,h,1===e,w);if(n)return n;if(f&&c===e-1){k=d.length;if(!k){if(g){g=0;c=-1;continue}return d}if(1===k)return sa(d[0],b,h)}}return la(d,b,h,f)};
function ra(a,b,c,d,e,f,h,g){let k=[],m=g?a.h:a.map;a.s||(m=ta(m,h,g,a.l));if(m){let n=0;const w=Math.min(m.length,g?a.A:a.D);for(let q=0,r=0,l,p;q<w;q++)if(l=m[q])if(a.s&&(l=ta(l,h,g,a.l)),e&&l&&f&&(p=l.length,p<=e?(e-=p,l=null):(l=l.slice(e),e=0)),l&&(k[n++]=l,f&&(r+=l.length,r>=d)))break;if(n){if(f)return sa(k,d,0);b[b.length]=k;return}}return!c&&k}function sa(a,b,c){a=1===a.length?a[0]:[].concat.apply([],a);return c||a.length>b?a.slice(c,c+b):a}
function ta(a,b,c,d){c?(d=d&&b>c,a=(a=a[d?b:c])&&a[d?c:b]):a=a[b];return a}t.contain=function(a){return!!this.register[a]};t.update=function(a,b){return this.remove(a).add(a,b)};
t.remove=function(a,b){const c=this.register[a];if(c){if(this.m)for(let d=0,e;d<c.length;d++)e=c[d],e.splice(e.indexOf(a),1);else O(this.map,a,this.D,this.s),this.depth&&O(this.h,a,this.A,this.s);b||delete this.register[a];if(this.cache){b=this.cache;for(let d=0,e,f;d<b.h.length;d++)f=b.h[d],e=b.cache[f],e.includes(a)&&(b.h.splice(d--,1),delete b.cache[f])}}return this};
function O(a,b,c,d,e){let f=0;if(a.constructor===Array)if(e)b=a.indexOf(b),-1!==b?1<a.length&&(a.splice(b,1),f++):f++;else{e=Math.min(a.length,c);for(let h=0,g;h<e;h++)if(g=a[h])f=O(g,b,c,d,e),d||f||delete a[h]}else for(let h in a)(f=O(a[h],b,c,d,e))||delete a[h];return f}t.searchCache=na;
t.export=function(a,b,c,d,e,f){let h=!0;"undefined"===typeof f&&(h=new Promise(m=>{f=m}));let g,k;switch(e||(e=0)){case 0:g="reg";if(this.m){k=x();for(let m in this.register)k[m]=1}else k=this.register;break;case 1:g="cfg";k={doc:0,opt:this.s?1:0};break;case 2:g="map";k=this.map;break;case 3:g="ctx";k=this.h;break;default:"undefined"===typeof c&&f&&f();return}qa(a,b||this,c,g,d,e,k,f);return h};
t.import=function(a,b){if(b)switch(C(b)&&(b=JSON.parse(b)),a){case "cfg":this.s=!!b.opt;break;case "reg":this.m=!1;this.register=b;break;case "map":this.map=b;break;case "ctx":this.h=b}};ka(L.prototype);function ua(a){a=a.data;var b=self._index;const c=a.args;var d=a.task;switch(d){case "init":d=a.options||{};a=a.factory;b=d.encode;d.cache=!1;b&&0===b.indexOf("function")&&(d.encode=Function("return "+b)());a?(Function("return "+a)()(self),self._index=new self.FlexSearch.Index(d),delete self.FlexSearch):self._index=new L(d);break;default:a=a.id,b=b[d].apply(b,c),postMessage("search"===d?{id:a,msg:b}:{id:a})}};let va=0;function P(a){if(!(this instanceof P))return new P(a);var b;a?E(b=a.encode)&&(a.encode=b.toString()):a={};(b=(self||window)._factory)&&(b=b.toString());const c="undefined"===typeof window&&self.exports,d=this;this.o=wa(b,c,a.worker);this.h=x();if(this.o){if(c)this.o.on("message",function(e){d.h[e.id](e.msg);delete d.h[e.id]});else this.o.onmessage=function(e){e=e.data;d.h[e.id](e.msg);delete d.h[e.id]};this.o.postMessage({task:"init",factory:b,options:a})}}Q("add");Q("append");Q("search");
Q("update");Q("remove");function Q(a){P.prototype[a]=P.prototype[a+"Async"]=function(){const b=this,c=[].slice.call(arguments);var d=c[c.length-1];let e;E(d)&&(e=d,c.splice(c.length-1,1));d=new Promise(function(f){setTimeout(function(){b.h[++va]=f;b.o.postMessage({task:a,id:va,args:c})})});return e?(d.then(e),this):d}}
function wa(a,b,c){let d;try{d=b?new (require("worker_threads")["Worker"])(__dirname + "/node/node.js"):a?new Worker(URL.createObjectURL(new Blob(["onmessage="+ua.toString()],{type:"text/javascript"}))):new Worker(C(c)?c:"worker/worker.js",{type:"module"})}catch(e){}return d};function S(a){if(!(this instanceof S))return new S(a);var b=a.document||a.doc||a,c;this.K=[];this.h=[];this.A=[];this.register=x();this.key=(c=b.key||b.id)&&T(c,this.A)||"id";this.m=u(a.fastupdate);this.C=(c=b.store)&&!0!==c&&[];this.store=c&&x();this.I=(c=b.tag)&&T(c,this.A);this.l=c&&x();this.cache=(c=a.cache)&&new K(c);a.cache=!1;this.o=a.worker;this.async=!1;c=x();let d=b.index||b.field||b;C(d)&&(d=[d]);for(let e=0,f,h;e<d.length;e++)f=d[e],C(f)||(h=f,f=f.field),h=D(h)?Object.assign({},a,h):a,
this.o&&(c[f]=new P(h),c[f].o||(this.o=!1)),this.o||(c[f]=new L(h,this.register)),this.K[e]=T(f,this.A),this.h[e]=f;if(this.C)for(a=b.store,C(a)&&(a=[a]),b=0;b<a.length;b++)this.C[b]=T(a[b],this.A);this.index=c}function T(a,b){const c=a.split(":");let d=0;for(let e=0;e<c.length;e++)a=c[e],0<=a.indexOf("[]")&&(a=a.substring(0,a.length-2))&&(b[d]=!0),a&&(c[d++]=a);d<c.length&&(c.length=d);return 1<d?c:c[0]}function U(a,b){if(C(b))a=a[b];else for(let c=0;a&&c<b.length;c++)a=a[b[c]];return a}
function V(a,b,c,d,e){a=a[e];if(d===c.length-1)b[e]=a;else if(a)if(a.constructor===Array)for(b=b[e]=Array(a.length),e=0;e<a.length;e++)V(a,b,c,d,e);else b=b[e]||(b[e]=x()),e=c[++d],V(a,b,c,d,e)}function X(a,b,c,d,e,f,h,g){if(a=a[h])if(d===b.length-1){if(a.constructor===Array){if(c[d]){for(b=0;b<a.length;b++)e.add(f,a[b],!0,!0);return}a=a.join(" ")}e.add(f,a,g,!0)}else if(a.constructor===Array)for(h=0;h<a.length;h++)X(a,b,c,d,e,f,h,g);else h=b[++d],X(a,b,c,d,e,f,h,g)}t=S.prototype;
t.add=function(a,b,c){D(a)&&(b=a,a=U(b,this.key));if(b&&(a||0===a)){if(!c&&this.register[a])return this.update(a,b);for(let d=0,e,f;d<this.h.length;d++)f=this.h[d],e=this.K[d],C(e)&&(e=[e]),X(b,e,this.A,0,this.index[f],a,e[0],c);if(this.I){let d=U(b,this.I),e=x();C(d)&&(d=[d]);for(let f=0,h,g;f<d.length;f++)if(h=d[f],!e[h]&&(e[h]=1,g=this.l[h]||(this.l[h]=[]),!c||!g.includes(a)))if(g[g.length]=a,this.m){const k=this.register[a]||(this.register[a]=[]);k[k.length]=g}}if(this.store&&(!c||!this.store[a])){let d;
if(this.C){d=x();for(let e=0,f;e<this.C.length;e++)f=this.C[e],C(f)?d[f]=b[f]:V(b,d,f,0,f[0])}this.store[a]=d||b}}return this};t.append=function(a,b){return this.add(a,b,!0)};t.update=function(a,b){return this.remove(a).add(a,b)};
t.remove=function(a){D(a)&&(a=U(a,this.key));if(this.register[a]){for(var b=0;b<this.h.length&&(this.index[this.h[b]].remove(a,!this.o),!this.m);b++);if(this.I&&!this.m)for(let c in this.l){b=this.l[c];const d=b.indexOf(a);-1!==d&&(1<b.length?b.splice(d,1):delete this.l[c])}this.store&&delete this.store[a];delete this.register[a]}return this};
t.search=function(a,b,c,d){c||(!b&&D(a)?(c=a,a=""):D(b)&&(c=b,b=0));let e=[],f=[],h,g,k,m,n,w,q=0;if(c)if(c.constructor===Array)k=c,c=null;else{a=c.query||a;k=(h=c.pluck)||c.index||c.field;m=c.tag;g=this.store&&c.enrich;n="and"===c.bool;b=c.limit||b||100;w=c.offset||0;if(m&&(C(m)&&(m=[m]),!a)){for(let l=0,p;l<m.length;l++)if(p=xa.call(this,m[l],b,w,g))e[e.length]=p,q++;return q?e:[]}C(k)&&(k=[k])}k||(k=this.h);n=n&&(1<k.length||m&&1<m.length);const r=!d&&(this.o||this.async)&&[];for(let l=0,p,A,B;l<
k.length;l++){let z;A=k[l];C(A)||(z=A,A=z.field,a=z.query||a,b=z.limit||b,g=z.enrich||g);if(r)r[l]=this.index[A].searchAsync(a,b,z||c);else{d?p=d[l]:p=this.index[A].search(a,b,z||c);B=p&&p.length;if(m&&B){const y=[];let H=0;n&&(y[0]=[p]);for(let W=0,oa,R;W<m.length;W++)if(oa=m[W],B=(R=this.l[oa])&&R.length)H++,y[y.length]=n?[R]:R;H&&(p=n?la(y,b||100,w||0):ma(p,y),B=p.length)}if(B)f[q]=A,e[q++]=p;else if(n)return[]}}if(r){const l=this;return new Promise(function(p){Promise.all(r).then(function(A){p(l.search(a,
b,c,A))})})}if(!q)return[];if(h&&(!g||!this.store))return e[0];for(let l=0,p;l<f.length;l++){p=e[l];p.length&&g&&(p=ya.call(this,p));if(h)return p;e[l]={field:f[l],result:p}}return e};function xa(a,b,c,d){let e=this.l[a],f=e&&e.length-c;if(f&&0<f){if(f>b||c)e=e.slice(c,c+b);d&&(e=ya.call(this,e));return{tag:a,result:e}}}function ya(a){const b=Array(a.length);for(let c=0,d;c<a.length;c++)d=a[c],b[c]={id:d,doc:this.store[d]};return b}t.contain=function(a){return!!this.register[a]};t.get=function(a){return this.store[a]};
t.set=function(a,b){this.store[a]=b;return this};t.searchCache=na;t.export=function(a,b,c,d,e,f){let h;"undefined"===typeof f&&(h=new Promise(g=>{f=g}));e||(e=0);d||(d=0);if(d<this.h.length){const g=this.h[d],k=this.index[g];b=this;setTimeout(function(){k.export(a,b,e?g:"",d,e++,f)||(d++,e=1,b.export(a,b,g,d,e,f))})}else{let g,k;switch(e){case 1:g="tag";k=this.l;c=null;break;case 2:g="store";k=this.store;c=null;break;default:f();return}qa(a,this,c,g,d,e,k,f)}return h};
t.import=function(a,b){if(b)switch(C(b)&&(b=JSON.parse(b)),a){case "tag":this.l=b;break;case "reg":this.m=!1;this.register=b;for(let d=0,e;d<this.h.length;d++)e=this.index[this.h[d]],e.register=b,e.m=!1;break;case "store":this.store=b;break;default:a=a.split(".");const c=a[0];a=a[1];c&&a&&this.index[c].import(a,b)}};ka(S.prototype);var Aa={encode:za,F:!1,G:""};const Ba=[G("[\u00e0\u00e1\u00e2\u00e3\u00e4\u00e5]"),"a",G("[\u00e8\u00e9\u00ea\u00eb]"),"e",G("[\u00ec\u00ed\u00ee\u00ef]"),"i",G("[\u00f2\u00f3\u00f4\u00f5\u00f6\u0151]"),"o",G("[\u00f9\u00fa\u00fb\u00fc\u0171]"),"u",G("[\u00fd\u0177\u00ff]"),"y",G("\u00f1"),"n",G("[\u00e7c]"),"k",G("\u00df"),"s",G(" & ")," and "];function za(a){var b=a=""+a;b.normalize&&(b=b.normalize("NFD").replace(da,""));return ba.call(this,b.toLowerCase(),!a.normalize&&Ba)};var Da={encode:Ca,F:!1,G:"strict"};const Ea=/[^a-z0-9]+/,Fa={b:"p",v:"f",w:"f",z:"s",x:"s","\u00df":"s",d:"t",n:"m",c:"k",g:"k",j:"k",q:"k",i:"e",y:"e",u:"o"};function Ca(a){a=za.call(this,a).join(" ");const b=[];if(a){const c=a.split(Ea),d=c.length;for(let e=0,f,h=0;e<d;e++)if((a=c[e])&&(!this.filter||!this.filter[a])){f=a[0];let g=Fa[f]||f,k=g;for(let m=1;m<a.length;m++){f=a[m];const n=Fa[f]||f;n&&n!==k&&(g+=n,k=n)}b[h++]=g}}return b};var Ha={encode:Ga,F:!1,G:""};const Ia=[G("ae"),"a",G("oe"),"o",G("sh"),"s",G("th"),"t",G("ph"),"f",G("pf"),"f",G("(?![aeo])h(?![aeo])"),"",G("(?!^[aeo])h(?!^[aeo])"),""];function Ga(a,b){a&&(a=Ca.call(this,a).join(" "),2<a.length&&(a=F(a,Ia)),b||(1<a.length&&(a=fa(a)),a&&(a=a.split(" "))));return a||[]};var Ka={encode:Ja,F:!1,G:""};const La=G("(?!\\b)[aeo]");function Ja(a){a&&(a=Ga.call(this,a,!0),1<a.length&&(a=a.replace(La,"")),1<a.length&&(a=fa(a)),a&&(a=a.split(" ")));return a||[]};I["latin:default"]=ia;I["latin:simple"]=Aa;I["latin:balance"]=Da;I["latin:advanced"]=Ha;I["latin:extra"]=Ka;const Y={Index:L,Document:S,Worker:P,registerCharset:function(a,b){I[a]=b},registerLanguage:function(a,b){ja[a]=b}};let Z;(Z=self.define)&&Z.amd?Z([],function(){return Y}):self.exports?self.exports=Y:self.FlexSearch=Y;}(this));

;
const search = document.querySelector('.search-input')
const suggestions = document.querySelector('.search-suggestions')
const background = document.querySelector('.search-background')

var index = new FlexSearch.Document({
  tokenize: "forward",
  cache: 100,
  document: {
    id: "id",
    tag: "tag",
    store: ["href", "title", "description"],
    index: ["title", "description", "content"]
  }
});

/*
Source:
  - https://github.com/nextapps-de/flexsearch#index-documents-field-search
  - https://raw.githack.com/nextapps-de/flexsearch/master/demo/autocomplete.html
*/
function initIndex() {
  // https://discourse.gohugo.io/t/range-length-or-last-element/3803/2
  // Note: pages without a title (such as browserconfig.xml) are excluded
  
  
  
  index.add(
    
      
      {
        id: 0,
        tag: "en",
        href: "/opensees-gallery/examples/archstaticsnap/",
        title: "Arch Instability",
        description: "Several nonlinear static analysis methods are used to investigate instabilities in a shallow arch.",
        
        
        content: "Incremental Analysis of a Shallow Arch \u0026nbsp; launchlaunchbinderbinder \u0026nbsp; Clarke, M.J. and Hancock, G.J. (1990) ‘A study of incremental‐iterative strategies for non‐linear analyses’, International Journal for Numerical Methods in Engineering, 29(7), pp. 1365–1391. Available at: https://doi.org/10.1002/nme.1620290702\u0026nbsp; .\nBegin by importing the arch_model helper function from the file arch.py:\nfrom arch import arch_modelImport some helpful third-party libraries\nimport numpy as np import matplotlib.pyplot as plt try: import scienceplots plt.style.use(\u0026#34;steel\u0026#34;) #([\u0026#34;ieee\u0026#34;, \u0026#34;science\u0026#34;, \u0026#34;notebook\u0026#34;]) except: pass The Framework \u0026nbsp; def analyze(model, mid, increment, steps, dx, *args): dof = 2 xy = [] status = 0 increment(model, mid, dof, dx, *args) for step in range(steps): if status != 0: dx /= 2 increment(model, mid, dof, dx, *args) status = model.analyze(1) xy.append([model.nodeDisp(mid, dof), model.getTime()]) return np.array(xy).TThe strategies used by Clarke and Hancock are:\nSolution 1 Iterative strategy: Constant load (Section 3.1) Load incrementation strategy: Direct incrementation of the load parameter (Section 4.1.1) Solution 2 Iterative strategy: Constant vertical displacement under the load, $v_6$ (Section 3.2) Load incrementation strategy: Incrementation of the displacement component $v_6$ (Section 4.1.2) Solution 3 Iterative strategy: Constant arc-length (Section 3.3) Load incrementation strategy: Incrementation of the arc-length (Section 4.1.3) Solution 4 Iterative strategy: Minimum unbalanced displacement norm (Section 3.5) Load incrementation strategy: Incrementation of the arc-length (Section 4.1.3) Solution 5 Iterative strategy: Constant weighted response (Section 3.7, equation (39)) Load incrementation strategy: Incrementation of the arc-length (Section 4.1.3) Solution 6 Iterative strategy: Minimum unbalanced force norm (Section 3.6) Load incrementation strategy: Using the current stiffness parameter (Section 4.2, equation (57)) Solution 7 Iterative strategy: Minimum unbalanced force norm (Section 3.6) Load incrementation strategy: Incrementation of the arc-length (Section 4.1.3) Solution 8 Iterative strategy: Constant arc-length (Section 3.3) Load incrementation strategy: Using the current stiffness parameter (Section 4.2, equation (57)) def solution0(model, mid, dof, dx): model.integrator(\u0026#34;LoadControl\u0026#34;, 400.0) def solution1(model, mid, dof, dx): Jd = 5 model.integrator(\u0026#34;LoadControl\u0026#34;, dx, Jd, -800., 800.) def solution2(model, mid, dof, dx): Jd = 5 model.integrator(\u0026#34;DisplacementControl\u0026#34;, mid, dof, dx, Jd) def norm_control(model, mid, dof, dx): Jd = 15 model.integrator(\u0026#34;MinUnbalDispNorm\u0026#34;, dx, Jd, -10, 10, \u0026#34;-det\u0026#34;) def arc_control(model, mid, dof, dx, a): model.integrator(\u0026#34;ArcLength\u0026#34;, dx, a, det=True, exp=0.5, reference=\u0026#34;point\u0026#34;)fig, ax = plt.subplots() # x, y = solution0(*arch_model(), 6, 400.0) # ax.plot(-x, y, \u0026#39;x\u0026#39;, label=\u0026#34;S0\u0026#34;) # x, y = analyze(*arch_model(), solution1, 6, 400.0) # ax.plot(-x, y, \u0026#39;x\u0026#39;, label=\u0026#34;S1\u0026#34;) # print(y) x, y = analyze(*arch_model(), solution2, 7, -150) ax.plot(-x, y, \u0026#39;o\u0026#39;, label=\u0026#34;S2\u0026#34;) x, y = analyze(*arch_model(), solution2, 536, -1.5) ax.plot(-x, y, \u0026#39;-\u0026#39;, label=\u0026#34;S2\u0026#34;) # x, y = analyze(*arch_model(), arc_control, 9500, 0.5, 0) # ax.plot(-x, y, \u0026#34;-\u0026#34;, label=\u0026#34;arc\u0026#34;) # Requires -det x, y = analyze(*arch_model(), arc_control, 110, 45, 0) ax.plot(-x, y, \u0026#34;x\u0026#34;, label=\u0026#34;arc\u0026#34;) x, y = analyze(*arch_model(), arc_control, 80, 88, 0) ax.plot(-x, y, \u0026#34;+\u0026#34;, label=\u0026#34;arc\u0026#34;) x, y = analyze(*arch_model(), arc_control, 80, 188, 0) ax.plot(-x, y, \u0026#34;*\u0026#34;, label=\u0026#34;arc\u0026#34;) # x, y = analyze(*arch_model(), arc_control, 8000, 0.8, 0) # ax.plot(-x, y, \u0026#34;x\u0026#34;, label=\u0026#34;arc\u0026#34;) # x, y = analyze(*arch_model(), norm_control, 7000, 1.0) # ax.plot(-x, y, \u0026#34;-\u0026#34;, label=\u0026#34;norm\u0026#34;) ax.set_xlim([0, 1200]) ax.set_ylim([-800, 3000]) fig.legend()Output:\n\u001b[0;31m FAILURE\u001b[0m :: Iter: 25, Norm: 49845.5, Norm deltaX: 152.498 \u001b[0;31m FAILURE\u001b[0m :: Iter: 25, Norm: 11340.8, Norm deltaX: 123.419 ArcLength::update() - imaginary roots due to multiple instability directions - initial load increment was too large a: 6.20586 b: -2674.5 c: 319258 b24ac: -772128 \u001b[0;31m FAILURE\u001b[0m :: Iter: 25, Norm: 3293.9, Norm deltaX: 54.5382\u0026lt;matplotlib.legend.Legend at 0x7f1ddb0b8d00\u0026gt; \u0026lt;Figure size 2560x1920 with 1 Axes\u0026gt;plt.plot(-x, \u0026#39;.\u0026#39;)Output:\n[\u0026lt;matplotlib.lines.Line2D at 0x7f1dd8e8ec40\u0026gt;] \u0026lt;Figure size 2560x1920 with 1 Axes\u0026gt;ax.plot(-x, \u0026#34;.\u0026#34;)Output:\n[\u0026lt;matplotlib.lines.Line2D at 0x7f1dd8cc8340\u0026gt;]The following animation of the solution is created in Animating.ipynb"
      })
      .add(
      
      
      {
        id: 1,
        tag: "en",
        href: "/opensees-gallery/examples/buildingmodes/",
        title: "Building Modes",
        description: "A building is modeled as a cantilever, and the first three mode shapes are plotted.",
        
        
        content: "This example is implemented in the following Python script, which can be downloaded from here: cantilever_modes.py.\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 # Import the opensees package for finite element analysis import opensees.openseespy as ops # Import some additional dependencies import matplotlib.pyplot as plt import numpy as np import pandas as pd plt.rcParams.update(\u0026#39;font.size\u0026#39;: 16) def make_model(): # Define a basic model with 2 dimensions and 3 degrees of freedom per node # (translation in X and Y directions, and rotation about the Z-axis) model = ops.Model(ndm=2, ndf=3) # # Define material # # Sets up an elastic material with given Young\u0026#39;s modulus (E), # moment of inertia (I), and cross-sectional area (A) E = 200e6 # Young\u0026#39;s modulus in kPa I = 0.0001 # Area moment of inertia in m^4 A = 0.01 # Cross-sectional area in m^2 model.uniaxialMaterial(\u0026#34;Elastic\u0026#34;, 1, E) # # Create nodes # # Nodes are created along a vertical line with a defined height between each, # representing floors of a building numFloors = 56 # Number of floors floorHeight = 3.0 # Height of each floor in meters for i in range(numFloors + 1): model.node(i + 1, 0, i * floorHeight) # Fix base node # The base node is fixed, meaning no translations or rotations are allowed, # mimicking a fixed foundation model.fix(1, 1, 1, 1) # Define geometric transformation (required for beam-column elements) ## A linear geometric transformation is defined for beam-column elements, ## essential for how elements behave in the model space model.geomTransf(\u0026#39;Linear\u0026#39;, 1) # Define elements (cantilever columns) # Beam-column elements are defined between each pair of nodes, # simulating the columns of a building for i in range(numFloors): nodes = (i + 1, i + 2) model.element(\u0026#34;ElasticBeamColumn\u0026#34;, i + 1, nodes, A, E, I, 1) # Define mass # Mass is assigned to each node (excluding the fixed base), # essential for dynamic analysis like modal analysis m = 2000 # Mass in kg for i in range(1, numFloors + 1): model.mass(i + 1, m, 1e-9, 0.0) # Mass assigned to each node return model, numFloors, floorHeight def plot_modes(model, numFloors, floorHeight): # Perform eigenvalue analysis # Eigenvalue analysis is performed to obtain the # first three natural frequencies and associated mode shapes numEigen = 3 eigenValues = model.eigen(numEigen) # Plotting fig, ax = plt.subplots(1, numEigen + 1, figsize=(15, 10), sharey=True, gridspec_kw=\u0026#39;wspace\u0026#39;: 0.1) # Floor height positions and labels for y-ticks floor_positions = [(i * floorHeight) for i in range(0, numFloors, 5)] # Every 5 floors floor_labels = [f\u0026#39;Fi\u0026#39; for i in range(1, numFloors + 1, 5)] # Every 5 floors for fp, fl in zip(floor_positions, floor_labels): print(f\u0026#39;Floor Position: fp - Floor Label: fl\u0026#39;) # Plot undeformed shape for i in range(numFloors): nodeTag_i = i + 1 nodeTag_j = i + 2 coord_i = model.nodeCoord(nodeTag_i) # Get the coordinates of the i-th node coord_j = model.nodeCoord(nodeTag_j) # Get the coordinates of the j-th node ax[0].plot([coord_i[0], coord_j[0]], [coord_i[1], coord_j[1]], \u0026#39;b-o\u0026#39;) ax[0].set_title(\u0026#39;Undeformed Shape\u0026#39;) ax[0].set_xlabel(\u0026#39;X\u0026#39;) # ax[0].set_ylabel(\u0026#39;Y\u0026#39;) ax[0].set_yticks(floor_positions) ax[0].set_yticklabels(floor_labels) # Adjust fontsize as needed # Plot mode shapes all_modal_displacements =  for mode in range(numEigen): for i in range(numFloors): nodeTag_i = i + 1 nodeTag_j = i + 2 coord_i = model.nodeCoord(nodeTag_i) # Get the coordinates of the i-th node coord_j = model.nodeCoord(nodeTag_j) # Get the coordinates of the j-th node ax[mode + 1].plot([coord_i[0], coord_j[0]], [coord_i[1], coord_j[1]], \u0026#39;-o\u0026#39;, color=\u0026#39;gray\u0026#39;) # get modal displacement and floor number for each node all_modal_displacements[mode] =  # Scale deformation to the node coordinates for easy visualization scaleFactor = 15 # Scale factor for deformation amplification for i in range(numFloors): nodeTag_i = i + 1 nodeTag_j = i + 2 coord_i = model.nodeCoord(nodeTag_i) coord_j = model.nodeCoord(nodeTag_j) eigenvector_i = model.nodeEigenvector(nodeTag_i, mode + 1) eigenvector_j = model.nodeEigenvector(nodeTag_j, mode + 1) # Apply scale factor to mode shape coord_i[0] += scaleFactor * eigenvector_i[0] coord_j[0] += scaleFactor * eigenvector_j[0] all_modal_displacements[mode][nodeTag_i] = coord_i[0] ax[mode + 1].plot([coord_i[0], coord_j[0]], [coord_i[1], coord_j[1]], \u0026#39;r-o\u0026#39;) print(f\u0026#39;Mode mode + 1 - Frequency: np.sqrt(eigenValues[mode]) / (2 * np.pi) Hz\u0026#39;) # print(f\u0026#39;Modal Displacements: modalDisplacements\u0026#39;) ax[mode + 1].set_title(f\u0026#39;Mode mode\u0026#39;) ax[mode + 1].set_xlabel(\u0026#39;X\u0026#39;) ax[mode + 1].set_ylim(ax[0].get_ylim()) # ax[mode + 1].set_yticks(floor_positions) # ax[mode + 1].set_yticklabels(floor_labels) ## Draw horizontal line at each floor level for a in ax: for y in floor_positions: a.axhline(y, color=\u0026#39;gray\u0026#39;, linestyle=\u0026#39;--\u0026#39;, linewidth=0.5) ## rotate x-axis labels for a in ax: plt.sca(a) plt.xticks(rotation=45) max_disp = 0.1 for a in ax: a.set_xlim([-max_disp, max_disp]) plt.savefig(\u0026#39;mode_shapes.png\u0026#39;, dpi=300, bbox_inches=\u0026#39;tight\u0026#39;) plt.close() # print(all_modal_displacements) ## all_modal_displacements to pandas dataframe df = pd.DataFrame(all_modal_displacements) # print(df.head()) ## ylocations for each mode yloc_offset = 0.1 ylocations = [i * yloc_offset for i in range(df.shape[1])] print(ylocations) fig, ax = plt.subplots(1, 1, figsize=(12, 8)) # plot for first mode ax.plot(df[0], \u0026#39;bo-\u0026#39;, label=\u0026#39;Mode 1\u0026#39;) ax.axhline(ylocations[0], color=\u0026#39;black\u0026#39;, linestyle=\u0026#39;--\u0026#39;, linewidth=1.0) ## plot for second mode with yaxis offset of 0.5 ax.plot(df[1] + ylocations[1], \u0026#39;ro-\u0026#39;, label=\u0026#39;Mode 2\u0026#39;) ax.axhline(ylocations[1], color=\u0026#39;black\u0026#39;, linestyle=\u0026#39;--\u0026#39;, linewidth=1.0) ## plot for third mode with yaxis offset of 1.0 ax.plot(df[2] + ylocations[2], \u0026#39;go-\u0026#39;, label=\u0026#39;Mode 3\u0026#39;) ax.axhline(ylocations[2], color=\u0026#39;black\u0026#39;, linestyle=\u0026#39;--\u0026#39;, linewidth=1.0) ax.set_xlabel(\u0026#39;Floor Number\u0026#39;) ax.set_ylabel(\u0026#39;Normalized Displacement\u0026#39;) ## xticks ax.set_xticks(range(1, numFloors + 1, 5)) ## yticks for each mode ax.set_yticks(ylocations) ax.set_yticklabels([f\u0026#39;Mode i\u0026#39; for i in range(len(ylocations))]) plt.savefig(\u0026#39;modal_displacements.png\u0026#39;, dpi=300, bbox_inches=\u0026#39;tight\u0026#39;) if __name__ == \u0026#39;__main__\u0026#39;: plot_modes(*make_model())"
      })
      .add(
      
      
      {
        id: 2,
        tag: "en",
        href: "/opensees-gallery/examples/cablestayed/",
        title: "Cable Stayed",
        description: "Model of a cable-stayed bridge imported from CSiBridge",
        
        
        content: "The problem is implemented in the file CableStayedBridge.py, and can also be run through the Tcl file CableStayedBridge.tcl."
      })
      .add(
      
      
      {
        id: 3,
        tag: "en",
        href: "/opensees-gallery/docs/configuration/colors/",
        title: "Colors",
        description: "Use Bootstrap's color system to easily adjust your website's colors.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 4,
        tag: "en",
        href: "/opensees-gallery/examples/frameshear/",
        title: "Columns with Nonlinear Geometry and Shear",
        description: "This example investigates P-Delta effects in columns with and without shear.",
        
        
        content: "Case_1.py Case_2.py This example implements the analysis presented in the AISC steel mannual.\nThe source code for this example is adapted from https://github.com/denavit/OpenSees-Examples\u0026nbsp;"
      })
      .add(
      
      
      {
        id: 5,
        tag: "en",
        href: "/opensees-gallery/docs/getting-started/command-line/",
        title: "Command line",
        description: "",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 6,
        tag: "en",
        href: "/opensees-gallery/docs/getting-started/compiling/",
        title: "Compiling",
        description: "Compiling your own version of OpenSees.",
        
        
        content: "Dependencies \u0026nbsp; Compiling OpenSees requires the following software to be installed on your local machine:\nSoftware Hugo Remarks Git\u0026nbsp; recommended Recommended for version control C/C++ Compilers \u0026nbsp; Embedded as npm binary Node.js\u0026nbsp; The installation package includes npm The primary system dependencies required for compiling are LAPACK/BLAS and Tcl. Packages providing these libraries are listed below for various package management ecosystems.\n\u0026nbsp; Note When building in an Anaconda environment, you should install all dependencies with conda or mamba, and preferably from the conda-forge channel. Expand the notes on Anaconda below.\nAnaconda (Mac, Windows, Linux) When using conda, you need to ensure that CMake only finds compilers that are compatible with the libraries in the environment. System compilers (like those installed by the operating system\u0026rsquo;s package manager) often cannot be used and can lead to segfaults. The following command should install everything you need:\nconda install -c conda-forge fortran-compiler cxx-compiler c-compiler openblas openmpi APT (Ubuntu, Debian Linux) Dependency Package LAPACK liblapack-dev BLAS libblas-dev Tcl* tcl-dev Pacman (Arch, Manjaro Linux) Dependency Package LAPACK lapack BLAS blas Tcl* tcl Yum (CentOS, Redhat Linux) Dependency Package LAPACK lapack-devel Tcl* tcl-devel Prerequisites \u0026nbsp; Clone the package repository: \u0026lt; command \u0026gt; git clone https://github.com/claudioperez/OpenSeesRT\u0026nbsp; \u0026lt; /command \u0026gt;\ninstall run-time dependencies. These are the libraries that will be needed in order to use OpenSees. To install these, run: \u0026lt; command \u0026gt; python -m pip install opensees \u0026lt; /command \u0026gt;\nInstall compile-time dependencies; see Dependencies below. These dependencies are only needed for the compilinf process.\nWindows installation notes \u0026nbsp; On Windows you should additionally install Intel compilers and Conan Compiling \u0026nbsp; The next steps describe how to set up your compilers and build the OpenSees library.\nCMake CMake\u0026amp;#43;Conan Create a directory to hold build artifacts\nmkdir build Configure the system for your system\ncd build cmake .. Start compiling\ncmake --build . --target OpenSees -j8 When libOpenSeesRT.so is compiled locally, the opensees package needs to be told where to find it. This can be done by setting an environment variable with the name OPENSEESRT_LIB to point to the location of libOpenSeesRT.so in the build tree. To this end, you may want to add a line like the following to your shell startup script (e.g., .bashrc):\nexport OPENSEESRT_LIB=\u0026#34;/path/to/your/compiled/libOpenSeesRT.so\u0026#34; Create a directory to hold build artifacts\nmkdir build cd build Run Conan\nconan install .. --build missing Configure the system for your system\ncmake .. Start compiling\ncmake --build . --target OpenSees -j8 When libOpenSeesRT.so is compiled locally, the opensees package needs to be told where to find it. This can be done by setting an environment variable with the name OPENSEESRT_LIB to point to the location of libOpenSeesRT.so in the build tree. To this end, you may want to add a line like the following to your shell startup script (e.g., .bashrc): export OPENSEESRT_LIB=\u0026#34;/path/to/your/compiled/libOpenSeesRT.so\u0026#34; Check that everything was built properly by running the following command:\npython -m openseesThis should start an OpenSees interpreter which can be closed by running the exit command.\n\u0026nbsp; Custom domain name Requires Azure CDN \u0026nbsp; CDN / Edge network Requires Azure CDN \u0026nbsp; HTTP headers Requires Azure CDN \u0026nbsp; ### Preparations The repository root should include a file `netlify.toml`. If not, copy it from the Hinode main repository\u0026nbsp; . The configuration file contains the build settings that Netlify will pick up when connecting to your repository. The panel below shows the default build settings. The key command to observe is `npm run build`, which ensures the site is built properly. \u003e [!NOTE] \u003e The default configuration provides basic security headers. Please review the [server configuration](/opensees-gallery/docs/getting-started/modeling/) for more details about the Content Security Policy. The cache settings are explained in more detail in the Netlify blog\u0026nbsp; . netlify.toml [build] publish = \u0026#34;exampleSite/public\u0026#34; command = \u0026#34;npm run build:example\u0026#34; [build.environment] DART_SASS_VERSION = \u0026#34;1.77.5\u0026#34; HUGO_VERSION = \u0026#34;0.131.0\u0026#34; HUGO_ENV = \u0026#34;production\u0026#34; HUGO_ENABLEGITINFO = \u0026#34;true\u0026#34; NODE_VERSION = \u0026#34;20.16.0\u0026#34; NPM_VERSION = \u0026#34;10.8.1\u0026#34; ... The same file also configures several optional plugins. netlify.toml [[plugins]] package = \u0026#34;@gethinode/netlify-plugin-dartsass\u0026#34; [[plugins]] package = \u0026#34;netlify-plugin-hugo-cache-resources\u0026#34; [plugins.inputs] # Redirected in exampleSite/config/_default/hugo.toml # srcdir = \u0026#34;\u0026#34; # [[plugins]] # package = \u0026#34;@netlify/plugin-lighthouse\u0026#34; # [plugins.inputs] # output_path = \u0026#34;reports/lighthouse.html\u0026#34; ... ### Configure your site Sign up for Netlify and configure your site in seven steps. Step 1. Sign up for Netlify Step 2. Sign in with your Git provider Step 3. Authenticate your sign in (2FA) Step 4. Add a new site Step 5. Connect to your Git provider Step 6. Import an existing project Step 7. Configure the build settings Previous Next Step 1. Sign up for Netlify Go to netlify.com\u0026nbsp; and click on the button Sign up. Select your preferred signup method next. This will likely be a hosted Git provider, although you also have the option to sign up with an email address. The next steps use GitHub, but other Git providers will follow a similar process. Step 2. Sign in with your Git provider Enter the credentials for your Git provider and click the button to sign in. Step 3. Authenticate your sign in (2FA) Assuming you have enabled two-factor authentication with your Git provider, authenticate the sign in next. This example uses the GitHub Mobile app. Step 4. Add a new site Click on the button Add new site to set up a new site with Netlify. Step 5. Connect to your Git provider Connect to your Git provider to import your existing Hinode repository. Step 6. Import an existing project Pick a repository from your Git provider. Ensure Netlify has access to the correct repository. Step 7. Configure the build settings Review the basic build settings. Netlify will use the settings provided in the preparations. Click on the button Deploy site to start the build and deployment process. Your site is now ready to be used. Click on the domain settings of your site within the `Site overview` page to provide a domain alias and to edit the site name as needed. The same section also allows the configuration of a custom domain. Be sure to review your [server configuration](/opensees-gallery/docs/getting-started/modeling/) if you encounter any rendering issues, such as broken links or garbled stylesheets. --\u003e"
      })
      .add(
      
      
      {
        id: 7,
        tag: "en",
        href: "/opensees-gallery/examples/concretesurface/",
        title: "Concrete",
        description: "An investigation of 3D concrete material models",
        
        
        content: "This example is adapted from the OpenSees documentation for the ASDConcrete material. The analysis is implemented in the Python scripts:\nASDConcrete3D_Ex_CyclicUniaxialCompression.py ASDConcrete3D_Ex_Surface.py ASDConcrete3D_MakeLaws.py"
      })
      .add(
      
      
      {
        id: 8,
        tag: "en",
        href: "/opensees-gallery/examples/example8/",
        title: "Continuum Cantilever",
        description: "Dynamic analysis of a cantilever beam, modeled with 8-node brick elements.",
        
        
        content: "In this example a simple problem in solid dynamics is considered. The structure is a cantilever beam modelled with three dimensional solid elements.\nExample8.tcl Example8.py For three dimensional analysis, a typical solid element is defined as a volume in three dimensional space. Each node of the analysis has three displacement degrees of freedom. Thus the model is defined with ndm = 3 and ndf = 3.\nFor this model, a mesh is generated using the block3D command. The number of nodes in the local xx -direction of the block is nx, the number of nodes in the local yy -direction of the block is ny and the number of nodes in the local zz -direction of the block is nz. The block3D generation nodes 1,2,3,4,5,6,7,8 are prescribed to define the three dimensional domain of the beam, which is of size 2×2×102 \\times 2 \\times 10 .\nTcl Python(RT) # mesh generation block3D $nx $ny $nz 1 1 $element $eleArgs  1 -1 -1 0 2 1 -1 0 3 1 1 0 4 -1 1 0 5 -1 -1 10 6 1 -1 10 7 1 1 10 8 -1 1 10  model.block3D(nx, ny, nz, 1, 1, Brick, 1,  1: [-1.0, -1.0, 0.0], 2: [ 1.0, -1.0, 0.0], 3: [ 1.0, 1.0, 0.0], 4: [-1.0, 1.0, 0.0], 5: [-1.0, -1.0, 10.0], 6: [ 1.0, -1.0, 10.0], 7: [ 1.0, 1.0, 10.0], 8: [-1.0, 1.0, 10.0]) Two possible brick elements can be used for the analysis. These may be created using the terms StdBrick or BbarBrick. An elastic isotropic material is used.\nFor initial gravity load analysis, a single load pattern with a linear time series and a single nodal loads is used.\nBoundary conditions are applied using the fixZ command. In this case, all the nodes whose zz -coordiate is 0.00.0 have the boundary condition 1,1,1, fully fixed.\nA solution algorithm of type Newton is used for the problem. The solution algorithm uses a ConvergenceTest which tests convergence on the norm of the energy increment vector. Five static load steps are performed.\nSubsequent to the static analysis, the wipeAnalysis and remove loadPatern commands are used to remove the nodal loads and create a new analysis. The nodal displacements have not changed. However, with the external loads removed the structure is no longer in static equilibrium.\nThe integrator for the dynamic analysis if of type GeneralizedMidpoint with α=0.5\\alpha = 0.5 . This choice is uconditionally stable and energy conserving for linear problems. Additionally, this integrator conserves linear and angular momentum for both linear and non-linear problems. The dynamic analysis is performed using 100100 time increments with a time step Δt=2.0\\Delta t = 2.0 .\nThe deformed shape at the end of the analysis is rendered below:\nThe results consist of the file cantilever.out, which contains a line for every time step. Each line contains the time and the horizontal displacement at the upper right corner the beam. This is plotted in the figure below:\n\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e"
      })
      .add(
      
      
      {
        id: 9,
        tag: "en",
        href: "/opensees-gallery/docs/getting-started/contribute/",
        title: "Contribute",
        description: "Contribute to the open-source development of OpenSees.",
        
        
        content: "OpenSees is fully open source and welcomes any contribution. To streamline the contribution process, please take a moment to review the guidelines outlined in this article.\nUsing the issue tracker \u0026nbsp; The issue tracker\u0026nbsp; on GitHub is the preferred channel for bug reports, feature requests and submitting pull requests.\nAsking for help \u0026nbsp; Use the GitHub Discussions\u0026nbsp; to ask for help from the OpenSees community\u0026nbsp; . The discussion forum also includes other topics, such as ideas\u0026nbsp; and showcases\u0026nbsp; . We strive for a safe, welcoming, and productive community. The community guidelines\u0026nbsp; provide more context about the expectations, moderation policy, and terms of service.\nBug reports \u0026nbsp; A bug is a demonstrable problem that is caused by the code in the repository. This may also include issues with the documentation or configuration files. Before filing a bug report, please consider the following guidelines:\nUse the GitHub issue search\u0026nbsp; — check if the issue has already been reported. Check if the issue has been fixed — try to reproduce it using the latest main in the repository\u0026nbsp; . Isolate the problem — ideally create a reduced test case. Use the provided template in the issue tracker\u0026nbsp; to capture the context, evidence and steps on how to reproduce the issue. Feature requests \u0026nbsp; Feature requests are welcome. Please use the provided template in the issue tracker\u0026nbsp; to capture the idea and context.\nPull requests \u0026nbsp; \u0026nbsp; Important By submitting a patch, you agree to allow the project owners to license your work under the terms of the BSD license\u0026nbsp; (if it includes code changes) and under the terms of the Creative Commons ( CC BY-NC 4.0)\u0026nbsp; license (if it includes documentation changes).\nPlease adhere to the coding guidelines used throughout the project (indentation, accurate comments, etc.) and any other requirements (such as test coverage).\nAdhering to the following process is the best way to get your work included in the project:\nFork the project, clone your fork, and configure the remotes:\ngit clone https://github.com/\u0026lt;your-username\u0026gt;/OpenSeesRT.git cd OpenSeesRT git remote add upstream https://github.com/claudioperez/OpenSeesRT If you cloned a while ago, get the latest changes from upstream:\ngit checkout main git pull upstream main Create a new topic branch (off the main project development branch) to contain your feature, change, or fix:\ngit checkout -b \u0026lt;topic-branch-name\u0026gt; Commit your changes in logical chunks. Please adhere to these git commit message guidelines\u0026nbsp; . Use Git\u0026rsquo;s interactive rebase\u0026nbsp; feature to tidy up your commits before making them public.\nLocally merge (or rebase) the upstream development branch into your topic branch:\ngit pull [--rebase] upstream main Push your topic branch up to your fork:\ngit push origin \u0026lt;topic-branch-name\u0026gt; Open a Pull Request\u0026nbsp; with a clear title and description against the main branch.\nCoding guidelines \u0026nbsp; In general, run clang-format \u0026lt;your-file.cpp\u0026gt; before committing to ensure your changes follow our coding standards.\nLicense \u0026nbsp; By contributing your code, you agree to license your contribution under the BSD license\u0026nbsp; . By contributing to the documentation, you agree to license your contribution under the Creative Commons ( CC BY-NC 4.0\u0026nbsp; ) license."
      })
      .add(
      
      
      {
        id: 10,
        tag: "en",
        href: "/opensees-gallery/docs/about/credits/",
        title: "Credits",
        description: "OpenSees is fully open source and uses several open-source frameworks and libraries.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 11,
        tag: "en",
        href: "/opensees-gallery/examples/soliddam/",
        title: "Dam",
        description: "",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 12,
        tag: "en",
        href: "/opensees-gallery/docs/developing/",
        title: "Developing",
        description: "Details about the internals of OpenSees.",
        
        
        content: "Class Interface Specification \u0026nbsp; Classes may be categorized as follows:\nDomain: These classes describe the finite element model and store the results of an analysis on the model. The classes include Domain, Element, Node, Load, SP_Constraint, MP_Constraint, and their subclasses.\nAnalysis: These classes perform the analysis of the finite element model. The classes include the Analysis, ConstraintHandler, DOF_Numberer, SolutionAlgorithm, Integrator, FE_Element, DOF_Group and AnalysisModel classes, and their subclasses.\nComputational Classes: These classes allow for composing efficient computational strategies that take advantage of prolem features such as sparsity, symmetry, and parallelism. More specifically these include:\nSystem of Equation These include the abstract SystemOfEquation and Solver classes, and subclasses of these classes. These classes are provided for the solving of large scale systems of linear and eigenvalue equations.\nGraph These are classes used to provide information about nodal and elemental connectivity and sparsity of systems of equations. The classes include Graph, Vertex, GraphNumberer, GraphPartitioner, and their subclasses. There is no Edge class provided at present. In current design each Vertex stores in an ID the tag of all it\u0026rsquo;s adjacent Vertices. For graph numbering and partitioning this has proved sufficient.\nParallel Classes These facilitate the development of parallel object-oriented finite element programs, classes are provided for parallel programming. The classes in the framework support the aggregate programming model. The classes include Actor, Shadow, Message, MachineBroker, FEM_ObjectBroker, Channel, and their subclasses.\nRuntime Classes: These include the ModelNamespace and G3_Runtime classes. An analyst will interact with a ModelBuilder object, to create the Element, Node, Load and Constraint objects that define the model.\nOther/Utility Classes\nMatrix Classes: These include the classes Matrix, Vector and ID (integer array). These classes are used in the framework for passing information between objects in a safe manner, and for small scale numerical calculations in element formulation.\nData Storage These are classes used to store data. There are two abstract classes TaggedObjectStorage and FE_Datastore. Objects of type TaggedObjectStorage are used as containers to store and provide access to the TaggedObjects in memory during program execution. FE_Datastore objects are used to store/retrieve information from databases, containers which can permanently hold program data.\nVisualization Classes These are classes used to generate images of the model for the analyst. These classes include Renderer, ColorMap, and their subclasses.\nThis design allows for contributions in the fields of:\nElement and material modeling.\nSolution algorithms, integration procedures and constraint handling techniques.\nModel generation.\nNumerical analysis for solution of linear and eigenvalue problems.\nGraph theory for numbering and partitioning graphs.\nData structures for container classes and database.\nGraphics.\nMessage passing systems and load balancing in parallel environments.\nFrank McKenna and Gregory L. Fenves December 20, 1999"
      })
      .add(
      
      
      {
        id: 13,
        tag: "en",
        href: "/opensees-gallery/examples/mrf_concentrated/",
        title: "Dynamic Analysis of 2-Story Moment Frame",
        description: "This example demonstrates how to perform a dynamic analysis in OpenSees using a 2-story, 1-bay steel moment resisting frame. The structure is subjected to the Canoga Park record from the 1994 Northridge earthquake. The nonlinear behavior is represented using the concentrated plasticity concept with rotational springs. The rotational behavior of the plastic regions follows a bilinear hysteretic response based on the Modified Ibarra Krawinkler Deterioration Model (Ibarra et al. 2005, Lignos and Krawinkler 2009, 2010). For this example, all modes of cyclic deterioration are neglected. A leaning column carrying gravity loads is linked to the frame to simulate P-Delta effects.\n",
        
        
        content: "This example demonstrates how to perform a dynamic analysis in OpenSees using a 2-story, 1-bay steel moment resisting frame. The structure is subjected to the Canoga Park record from the 1994 Northridge earthquake. The nonlinear behavior is represented using the concentrated plasticity concept with rotational springs. The rotational behavior of the plastic regions follows a bilinear hysteretic response based on the Modified Ibarra Krawinkler Deterioration Model (Ibarra et al. 2005, Lignos and Krawinkler 2009, 2010). For this example, all modes of cyclic deterioration are neglected. A leaning column carrying gravity loads is linked to the frame to simulate P-Delta effects.\nThe files needed to analyze this structure in OpenSees are included here:\nThe main file: MRF_2Story_Concentrated.tcl (last update: 10 Oct 2013) Supporting procedure files\nRotSpring2DModIKModel.tcl - creates a bilinear rotational spring that follows the Modified Ibarra Krawinkler Deterioration Model (used in the concentrated model) RotLeaningCol.tcl - creates a low-stiffness rotational spring used in a leaning column The acceleration history for the Canoga Park record\nNR94cnp.tcl - contains acceleration history in units of g All files are available in a compressed format here: dynamic_example_10Oct2013.zip (last update: 10 Oct 2013)\nThe rest of this example describes the model and shows the analysis results.\nModel Description Figure 1. Schematic representation of concentrated plasticity OpenSees model with element number labels and [node number] labels. Note: The springs are zeroLength elements, but their sizes are greatly exaggerated in this figure for clarity. The 2-story, 1-bay steel moment resisting frame is modeled with elastic beam-column elements connected by ZeroLength elements which serve as rotational springs to represent the structure’s nonlinear behavior. The springs follow a bilinear hysteretic response based on the Modified Ibarra Krawinkler Deterioration Model. A leaning column with gravity loads is linked to the frame by truss elements to simulate P-Delta effects. An idealized schematic of the model is presented in Figure 1.\nTo simplify this model, panel zone contributions are neglected, plastic hinges form at the beam-column joints, and centerline dimensions are used. For an example that explicitly models the panel zone shear distortions and includes reduced beam sections (RBS), see Pushover and Dynamic Analyses of 2-Story Moment Frame with Panel Zones and RBS.\nFor a detailed description of this model, see Pushover Analysis of 2-Story Moment Frame. The units of the model are kips, inches, and seconds.\nDamping and the Rayleigh Command This model uses Rayleigh damping which formulates the damping matrix as a linear combination of the mass matrix and stiffness matrix: c = a0m + a1k, where a0 is the mass proportional damping coefficient and a1 is the stiffness proportional damping coefficient. A damping ratio of 2%, which is a typical value for steel buildings, is assigned to the first two modes of the structure. The rayleigh command allows the user to specify whether the initial, current, or last committed stiffness matrix is used in the damping matrix formulation. In this example, only the initial stiffness matrix is used, which is accomplished by assigning values of 0.0 to the other stiffness matrix coefficients.\nTo properly model the structure, stiffness proportional damping is applied only to the frame elements and not to the highly rigid truss elements that link the frame and leaning column, nor to the leaning column itself. OpenSees does not apply stiffness proportional damping to zeroLength elements. In order to apply damping to only certain elements, the rayleigh command is used in combination with the region command. As noted in the region command documentation, the region cannot be defined by BOTH elements and nodes. Because mass proportional damping assigns damping to nodes with mass, OpenSees will ignore any mass proportional damping that is assigned using the rayleigh command in combination with the region command for a region of elements. Therefore, if using the region command to assign damping, the mass proportional damping and stiffness proportional damping must be assigned in separate steps.\nModifications to the Stiffness Proportional Damping Coefficient As described in the “Stiffness Modifications to Elastic Frame Elements” section of Pushover Analysis of 2-Story Moment Frame, the stiffness of the elastic frame elements has been modified. As explained in Ibarra and Krawinkler (2005) and Zareian and Medina (2010), the stiffness proportional damping coefficient that is used with these elements must also be modified. As the stiffness of the elastic elements was made “(n+1)/n” times greater than the stiffness of the actual frame member, the stiffness proportional damping coefficient of these elements must also be made “(n+1)/n” times greater than the traditional stiffness proportional damping coefficient.\nDynamic Analysis Recorders The recorders used in this example include:\nThe drift recorder to track the story and roof drift histories The node recorder to track the floor displacement and base shear reaction histories The element recorder to track the element forces in the first story columns as well as the moment and rotation histories of the springs in the concentrated plasticity model For the element recorder, the region command was used to assign all column springs to one group and all beam springs to a separate group.\nIt is important to note that the recorders only record information for analyze commands that are called after the recorder commands are called. In this example, the recorders are placed after the gravity analysis so that the steps of the gravity analysis do not appear in the output files.\nAnalysis The structure is analyzed under gravity loads before the dynamic analysis is conducted. The gravity loads are applied using a load-controlled static analysis with 10 steps. So that the gravity loads remain on the structure for all subsequent analyses, the loadConst command is used after the gravity analysis is completed. This command is also used to reset the time to zero so that the dynamic analysis starts from time zero.\nFor the dynamic analysis, the structure is subjected to the Canoga Park record from the 1994 Northridge earthquake. To apply the ground motion to the structure, the uniform excitation pattern is used. The name of the file containing the acceleration record, timestep of the ground motion, scale factor applied to the ground motion, and the direction in which the motion is to be applied must all be specified as part of the uniform excitation pattern command.\nTo execute the dynamic analysis, the analyze command is used with the specified number of analysis steps and the timestep of the analysis. The timestep used in the analysis should be less than or equal to the timestep of the input ground motion.\nResults Figure 2. Floor Displacement History The floor displacement histories from the dynamic analysis are shown in Figure 2. The top graph shows the ground acceleration history while the middle and bottom graphs show the displacement time histories of the 3rd floor (roof) and 2nd floor, respectively.\nReferences Ibarra, L. F., and Krawinkler, H. (2005). “Global collapse of frame structures under seismic excitations,” Technical Report 152, The John A. Blume Earthquake Engineering Research Center, Department of Civil Engineering, Stanford University, Stanford, CA. [electronic version: https://blume.stanford.edu/tech_reports] Ibarra, L. F., Medina, R. A., and Krawinkler, H. (2005). “Hysteretic models that incorporate strength and stiffness deterioration,” Earthquake Engineering and Structural Dynamics, Vol. 34, 12, pp. 1489-1511. Lignos, D. G., and Krawinkler, H. (2009). “Sidesway Collapse of Deteriorating Structural Systems under Seismic Excitations,” Technical Report 172, The John A. Blume Earthquake Engineering Research Center, Department of Civil Engineering, Stanford University, Stanford, CA. Lignos, D. G., and Krawinkler, H. (2011). “Deterioration Modeling of Steel Beams and Columns in Support to Collapse Prediction of Steel Moment Frames,” ASCE, Journal of Structural Engineering, Vol. 137 (11), 1291-1302. Zareian, F. and Medina, R. A. (2010). “A practical method for proper modeling of structural damping in inelastic plane structural systems,” Computers \u0026amp; Structures, Vol. 88, 1-2, pp. 45-53. Example posted by: Laura Eads, Stanford University; Modified: Filipe Ribeiro, Andre Barbosa (09/03/2013)"
      })
      .add(
      
      
      {
        id: 14,
        tag: "en",
        href: "/opensees-gallery/examples/example7/",
        title: "Dynamic Shell Analysis",
        description: "Transient analysis of a shell model.",
        
        
        content: "In this example a simple problem in shell dynamics is considered. The structure is a curved hoop shell structure that looks like the roof of a Safeway.\nExample7.tcl Example7.py Renderings are created from the script render.py, which uses the sees\u0026nbsp; Python package.\nModeling \u0026nbsp; For shell analysis, a typical shell element is defined as a surface in three dimensional space. Each node of a shell analysis has six degrees of freedom, three displacements and three rotations. Thus the model is defined with ndm=3ndm = 3 and ndf=6ndf = 6 .\nFor this model, a mesh is generated using the block2D command. The number of nodes in the local x-direction of the block is nx and the number of nodes in the local y-direction of the block is ny. The block2D generates nodes with tags 1,2,3,4, 5,7,9 such that the structure is curved in space.\nTcl Python(RT) # generate the nodes and elements block2D $nx $ny 1 1 $element $eleArgs  1 -20 0 0 2 -20 0 40 3 20 0 40 4 20 0 0 5 -10 10 20 7 10 10 20 9 0 10 20  # generate the surface nodes and elements surface = model.surface((nx, ny), element=\u0026#34;ShellMITC4\u0026#34;, args=(1,), points= 1: [-20.0, 0.0, 0.0], 2: [-20.0, 0.0, 40.0], 3: [ 20.0, 0.0, 40.0], 4: [ 20.0, 0.0, 0.0], 5: [-10.0, 10.0, 20.0], 7: [ 10.0, 10.0, 20.0], 9: [ 0.0, 10.0, 20.0] ) The shell element is constructed using the ShellMITC4 formulation. An elastic membrane-plate material section model, appropriate for shell analysis, is constructed using the section command and the \u0026quot;ElasticMembranePlateSection\u0026quot; formulation. In this case, the elastic modulus E=3.0e3E = 3.0e3 , Poisson\u0026rsquo;s ratio ν=0.25\\nu = 0.25 , the thickness h=1.175h = 1.175 and the mass density per unit volume ρ=1.27\\rho = 1.27 Boundary conditions are applied using the fixZ command. In this case, all the nodes whose zz -coordiate is 0.00.0 have the boundary condition 1,1,1, 0,1,1: all degrees-of-freedom are fixed except rotation about the x-axis, which is free. The same boundary conditions are applied where the zz -coordinate is 40.040.0 .\nA solution algorithm of type Newton is used for the problem. The solution algorithm uses a ConvergenceTest which tests convergence on the norm of the energy increment vector. Five static load steps are performed.\nFor initial gravity load analysis, a single load pattern with a linear time series and three vertical nodal loads are used. A scaled rendering of the deformed shape under gravity loading is shown below:\nDynamic Analysis \u0026nbsp; After the static analysis, the wipeAnalysis and remove loadPatern commands are used to remove the nodal loads and create a new analysis. The nodal displacements have not changed. However, with the external loads removed the structure is no longer in static equilibrium.\nThe integrator for the dynamic analysis if of type GeneralizedMidpoint with α=0.5\\alpha = 0.5 . This choice is uconditionally stable and energy conserving for linear problems. Additionally, this integrator conserves linear and angular momentum for both linear and non-linear problems. The dynamic analysis is performed using 250250 time increments with a time step Δt=0.50\\Delta t = 0.50 .\nThe results consist of the file Node.out, which contains a line for every time step. Each line contains the time and the vertical displacement at the upper center of the hoop structure. The time history is shown in the figure below.\n\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e"
      })
      .add(
      
      
      {
        id: 15,
        tag: "en",
        href: "/opensees-gallery/examples/thermalexamples/thermalexample1/",
        title: "Example 1",
        description: "Thermal expansion of a beam \u0026nbsp; {.align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;}\n",
        
        
        content: "Thermal expansion of a beam \u0026nbsp; .align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nElevation of beam\nExample Overview: A steel beam is heated to 1180 ° C. Horizontal displacement of right end is recorded. This displacement is normalized against the original length and plotted against temperature. The calculated thermal expansion is compared against the steel temperature-dependent thermal expansion in Eurocode 3, Part 1-2 11 .\nDownload Example 1 files:\nExample1.tcl\nExample 1 Outputs \u0026lt;files/Example1_OUTPUT.zip\u0026gt;.interpreted-text role=\u0026ldquo;download\u0026rdquo;.\nMaterial Properties \u0026nbsp; The uniaxialMaterial Steel01Thermal includes temperature-dependent steel thermal and mechanical properties per Eurocode 3 11 . More details of Steel01 can be found at: Steel01 Material\u0026nbsp; uniaxialMaterial Steel01Thermal $matTag $Fy $Es $b;Es = 210 GPa (Young\u0026rsquo;s modulus of elasticity at ambient temperatures)\nFy = 250 MPa (Yield strength of material at ambient temperatures)\nb = 0.001 (Strain-Hardening Ratio)\nTransformation \u0026nbsp; The beam is expanding in one direction, therefore, 2nd order bending effects do not need to be considered.\ngeomTransf Linear $transftag;Learn more about geometric transofrmations: Geometric Transformation\u0026nbsp; Section \u0026nbsp; The discretization of the steel section into four fibers is shown using the code below:\nsection FiberThermal secTag -GJ $Esset numSubdivIJ 2; \\# horizontalset numSubdivJK 2; \\# verticalset yI -100; #mmset zI -200; #mmset yJ 100; #mmset zJ -200; #mmset yK 100; #mmset zK 200; #mmset yL -100; #mmset zL 200; #mmpatch quad $matTag $numSubdivIJ $numSubdivJK $yI $zI $yJ $zJ $yK $zK $yL $zLSections that will be subjected to thermal loading must be created with fiberThermal or fibersecThermal.\nIn previous versions of OpenSees, a default value for torsional stiffness was used (GJ). In versions 3.1.0 and newer fiber sections require a value for torsional stiffness. This is a 2D example with negligible torsion, however a value is required. The Young's Modulus is used for convenience.\nThe discretization can be visualized as such:\n.align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nCross section of rectangular beam showing fiber discretization\nElements \u0026nbsp; dispBeamColumnThermal elements are used because temperature-dependent thermal and mechanical steel properties can be applied to these elements. Any portion of the structure that is being heated must use elements that are compatible with uniaxialMaterial Steel01Thermal. At the time this model was developed, dispBeamColumnThermal was the only element type that could have tempurature-dependent thermal and mechanical properties applied to them.\nThe beam is made of one element with 5 iteration points and connects nodes 1 \u0026amp; 2. OpenSees is sensitive to the number of iteration points in each element and this could change the result of the recorded displacement. For this reason, it is important to perform these benchmarking examples to establish how many iteration points allows for convergence to the expected recorded displacement. To code the number of iteration points, we use the following syntax:\ndispBeamColumnThermal eleTag iNode jNode numIntgrPts secTag TransfTag;\nelement dispBeamColumnThermal 1 1 2 5 $secTag $transftag; Output Recorders \u0026nbsp; Displacement of the end node (2) in DOF 1 (Horizontal Displacement) is what we want to record. To do so, a folder within your working directory must be created. dataDir is the command to create that folder and should be defined at the beginning of the model. This is where your output files will be saved.\nset dataDir Examples/EXAMPLE2_OUTPUT;file mkdir $dataDir;recorder Node -file $dataDir/Node2disp.out -time -node 2 -dof 1 disp;Learn more about the Recorder Command: [ Recorder Command \u0026lt;http://opensees.berkeley.edu/wiki/index.php/Recorder_Command\u0026gt;].title-ref __\nThermal Loading \u0026nbsp; This particular model is heating a beam to a set temperature over the time period of the model. We are not asking OpenSees to use a specific time-temperature curve, rather linearly ramp up the temperature from ambient to 1180 ° C.\nTherefore, we set the maximum temperature as follows:\nT = Max Tempurature degcelciusdeg celcius set T 1180;In OpenSees, the user can define 2 or 9 temperature data points through the cross section. In a 2D analysis framework, like this example, temperature data point locations are specified on the y-axis of the local coordinate system (as shown in the figure below), and are linearly interpolated between the defined points. Because this example is using a uniformly heated beam, the entire cross section is one temperature, and two temperature points on each extreme fiber on the y-axis will be chosen. The beam has a depth of 400 mm, therefore, Y1 = 200 mm \u0026amp; Y2 = -200 mm for the top and bottom fibers respectively.\nLocation of bottom extreme fiber of beam mmmm set Y1 100;Location of top extreme fiber of beam mmmm set Y2 -100; .align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nLocation of defined input temperature locations on the member cross section\nThe bottom extreme fiber temperature must be defined first. The target maximum temperature for each extreme fiber is set to 1180\u0026lt;sup\u0026gt;o\u0026lt;/sup\u0026gt;C and will be increased incrementally and linearly as the time step continues in the analysis. An external temperature data set could also be used for more complex temperature loading. The syntax for this is:\nThermal loading pattern\npattern Plain 1 Linear  eleLoad -ele 1 -type -beamThermal $T $Y2 $T $Y1 ; Thermal Analysis \u0026nbsp; Thermal loading is applied in 1000 steps, with a load factor of 0.001. Each step is a 0.001 increment of the maximum temperature specified in the thermal loading step: T. The analysis is a static analysis and the contraints of the beam are plain. 1000 increments was also used during thermal analysis to allow for easy correlation between the input temperatures and the recorded output.\nA variety of load factors were examined and the solution converged when a load factor of 0.001 was used. OpenSees is sensitive to the load factor, therefore, it is important to ensure that benchmarking examples are performed to determine the proper load factor to use in structural fire engineering analyses.\nset Nsteps 1000set Factor \\[expr 1.0/$Nsteps\\];integrator LoadControl $Factor;analyze $Nsteps; Output Plots \u0026nbsp; After the model has completed running, the results will be a horizontal displacement of the right end of the beam. Since the temperature was linearly ramped up from ambient to 1180 ° C, the user can develop a temperature history that matches every increment of the model.\nThermal expansion is the change is length divided by the original length. This could also be called thermal strain. The thermal expansion of the beam is plotted below and compared to the Eurocode 3 11 temperature-dependent thermal expansion. We can see that the modeled thermal expansion matches the material properties. This is important to check that the temperatures and material properties are assigned propertly in the model.\n.align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nThermal expansion of the beam recorded at node 2\nSources \u0026nbsp; 11 European Committee for Standardization (CEN). (2005). Eurocode 3: Design of Steel Structures, Part 1.2: General Rules - Structural Fire Design."
      })
      .add(
      
      
      {
        id: 16,
        tag: "en",
        href: "/opensees-gallery/examples/example1/",
        title: "Example 1: Linear Truss",
        description: "A finite element model of a simple truss is created, and static analysis is performed.",
        
        
        content: "\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e This example is of a linear-elastic three bar truss, as shown in the figure above, subject to static loads. The purpose of this example is to develop the basic requirements for performing finite element analysis with OpenSees. This includes the definition of nodes, materials, elements, loads and constraints.\nScripts for this example can be downloaded for either Python or Tcl:\nExample1.py Example1.tcl Model \u0026nbsp; We begin the simulation by creating a Model, which will manage the nodes, elements, loading and state. This is done through either Python or Tcl as follows:\nTcl Python(RT) model -ndm 2 -ndf 2 import opensees.openseespy as ops model = ops.Model(ndm=2, ndf=2) where we\u0026rsquo;ve specified 2 for the spatial dimension ndm, and 2 for the number of degrees of freedom ndf.\nNext we define the four nodes of the structural model by specifying a tag which identifies the node, and coordinates in the x−yx-y plane. In general, the node constructor must be passed ndm coordinates.\nTcl Python(RT) # Create nodes \u0026amp; add to domain # tag X Y node 1 0.0 0.0; node 2 144.0 0.0; node 3 168.0 0.0; node 4 72.0 96.0; # Create nodes # tag X Y model.node(1, 0.0, 0.0) model.node(2, 144.0, 0.0) model.node(3, 168.0, 0.0) model.node(4, 72.0, 96.0) The restraints at the nodes with reactions (ie, nodes 1, 2, and 3) are then defined.\nTcl Python(RT) # Set the boundary conditions # tag X Y fix 1 1 1; fix 2 1 1; fix 3 1 1; # set the boundary conditions # nodeID xRestrnt? yRestrnt? model.fix(1, 1, 1) model.fix(2, 1, 1) model.fix(3, 1, 1) Since the truss elements have the same elastic material, a single Elastic material object is created. The first argument assigns the tag 1 to the material, and the second specifies a Young\u0026rsquo;s modulus of 3000.\nTcl Python(RT) # Create Elastic material prototype uniaxialMaterial Elastic 1 3000; # Create Elastic material prototype model.uniaxialMaterial(\u0026#34;Elastic\u0026#34;, 1, 3000) Finally, define the elements. The syntax for creating the truss element requires the following arguments:\nthe element name, in this case always \u0026quot;Truss\u0026quot;, the element tag, in this case 1 through 3, the nodes that the element is connected to, the cross-sectional area, in this case 10.0 for element 1 and 5.0 for elements 2 and 3. the tag of the material assigned to the element, in this case always 1 Tcl Python(RT) element Truss 1 1 4 10.0 1; element Truss 2 2 4 5.0 1; element Truss 3 3 4 5.0 1; # Type tag nodes Area material model.element(\u0026#34;Truss\u0026#34;, 1, (1, 4), 10.0, 1 ) model.element(\u0026#34;Truss\u0026#34;, 2, (2, 4), 5.0, 1 ) model.element(\u0026#34;Truss\u0026#34;, 3, (3, 4), 5.0, 1 ) Loads \u0026nbsp; The final step before we can configure and run the analysis is to define some loading. In this case we have two point loads at the apex of the truss (node 4). In OpenSees, loads are assigned to load patterns, which define how loads are scaled with each load step. In Python, the simplest way to represent a nodal load is by a dictionary with node numbers as keys, and corresponding load vector as values. For the problem at hand, we want to apply a load to node 4 with 100 units in the xx direction, and -50 units in the yy direction; the corresponding definition is: Tcl Python(RT) set loads 4 100 -50 loads = 4: [100, -50] We then add a \u0026quot;Plain\u0026quot; load pattern to the model with these loads, and use the \u0026quot;Linear\u0026quot; option to specify that it should be increased linearly with each new load step. Tcl Python(RT) pattern Plain 1 \u0026#34;Linear\u0026#34; \u0026#34;load $loads\u0026#34; model.pattern(\u0026#34;Plain\u0026#34;, 1, \u0026#34;Linear\u0026#34;, load=loads) Note that it is common to define the load data structure inside the call to the pattern function. This looks like:\nTcl Python(RT) pattern Plain 1 \u0026#34;Linear\u0026#34;  load 4 100 -50  model.pattern(\u0026#34;Plain\u0026#34;, 1, \u0026#34;Linear\u0026#34;, load= 4: [100, -50] ) Analysis \u0026nbsp; Next we configure that analysis procedure. The model is linear, so we use a solution Algorithm of type Linear.\nTcl Python(RT) algorithm Linear; model.algorithm(\u0026#34;Linear\u0026#34;) Even though the solution is linear, we have to select a procedure for applying the load, which is called an Integrator. For this problem, a LoadControl integrator is selected, which advances the solution by incrementing the applied loads by a factor of 1.0 each time the analyze command is called.\nTcl Python(RT) integrator LoadControl 1.0; model.integrator(\u0026#34;LoadControl\u0026#34;, 1.0) The equations are formed using a banded system, so the System is BandSPD (banded, symmetric positive definite). This is a good choice for most moderate size models. The equations have to be numbered, so typically an RCM numberer object is used (for Reverse Cuthill-McKee). The constraints are most easily represented with a Plain constraint handler.\nOnce all the components of an analysis are defined, the Analysis itself is defined. For this problem a Static analysis is used.\nTcl Python(RT) analysis Static; model.analysis(\u0026#34;Static\u0026#34;) Finally, one analysis step is performed by invoking analyze: Tcl Python(RT) analyze 1 model.analyze(1) When the analysis is complete the state of node 4 and all three elements may be printed to the screen:\nTcl Python(RT) print node 4 print ele model.print(node=4) model.print(\u0026#34;ele\u0026#34;) Node: 4 Coordinates : 72 96 commitDisps: 0.530093 -0.177894 unbalanced Load: 100 -50 Element: 1 type: Truss iNode: 1 jNode: 4 Area: 10 Total Mass: 0 strain: 0.00146451 axial load: 43.9352 unbalanced load: -26.3611 -35.1482 26.3611 35.1482 Material: Elastic tag: 1 E: 3000 eta: 0 Element: 2 type: Truss iNode: 2 jNode: 4 Area: 5 Total Mass: 0 strain: -0.00383642 axial load: -57.5463 unbalanced load: -34.5278 46.0371 34.5278 -46.0371 Material: Elastic tag: 1 E: 3000 eta: 0 Element: 3 type: Truss iNode: 3 jNode: 4 Area: 5 Total Mass: 0 strain: -0.00368743 axial load: -55.3114 unbalanced load: -39.1111 39.1111 39.1111 -39.1111 Material: Elastic tag: 1 E: 3000 eta: 0For the node, displacements and loads are given. For the truss elements, the axial strain and force are provided along with the resisting forces in the global coordinate system.\nThe file example.out, specified in the recorder command, provides the nodal displacements for the xx and yy directions of node 4. The file consists of a single line:\n1.0 0.530093 -0.177894 The 1.01.0 corresponds to the load factor (pseudo time) in the model at which point the recorder was invoked. The 0.5300930.530093 and −0.177894-0.177894 correspond to the response at node 4 for the 1 and 2 degree-of-freedom. Note that if more analysis steps had been performed, the line would contain a line for every analysis step that completed successfully."
      })
      .add(
      
      
      {
        id: 17,
        tag: "en",
        href: "/opensees-gallery/examples/thermalexamples/thermalexample2/",
        title: "Example 2",
        description: "Restrained Steel beam subjected to uniform temperature on half of the member. \u0026nbsp; {.align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;}\n",
        
        
        content: "Restrained Steel beam subjected to uniform temperature on half of the member. \u0026nbsp; .align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nExample overview: A steel beam of two equal elements is subjected to a uniform temperature on only one of the elements. Element 1 remains at ambient tempurature while Element 2 is heated using a linear time-temperature history.\nDownload Example 2 files:\nExample2.tcl\nExample 2 Outputs \u0026lt;files/EXAMPLE2_OUTPUT.zip\u0026gt;.interpreted-text role=\u0026ldquo;download\u0026rdquo;.\nObjective \u0026nbsp; Example 2 Objectives:\nDevelop a simply supported steel beam using displacement-based beam elements with tempurature-dependent material properites, Record internal forces of an element subjected to a linear time-temperature history due to the restraint against thermal expansion, Record displacement of a node due to a linear time-temperature history, and Correlate the recorded internal forces and displacement with the linear time-temperature history to plot the two variables as a function of temperature. Material \u0026nbsp; The uniaxialMaterial Steel01Thermal includes temperature-dependent steel thermal and mechanical properties per Eurocode 3 11 . More details of Steel01 can be found at: Steel01 Material\u0026nbsp; uniaxialMaterial Steel01Thermal $matTag $Fy $Es $b;Es = 210 GPa (Young\u0026rsquo;s modulus of elasticity at ambient temperatures)\nFy = 250 MPa (Yield strength of material at ambient temperatures)\nb = 0.001 (Strain-Hardening Ratio)\nTransformation \u0026nbsp; The beam is expanding in one direction, therefore, 2nd order bending effects do not need to be considered.\ngeomTransf Linear $transftag;Learn more about geometric transofrmations: Geometric Transformation\u0026nbsp; Section \u0026nbsp; The discretization of the steel section into four fibers is shown using the code below:\nsection FiberThermal secTag -GJ $Esset numSubdivIJ 2; \\# horizontal divisionset numSubdivJK 2; \\# vertical divisionset yI -100; #mmset zI -200; #mmset yJ 100; #mmset zJ -200; #mmset yK 100; #mmset zK 200; #mmset yL -100; #mmset zL 200; #mmpatch quad $matTag $numSubdivIJ $numSubdivJK $yI $zI $yJ $zJ $yK $zK $yL $zLSections that will be subjected to thermal loading must be created with fiberThermal or fibersecThermal.\nIn previous versions of OpenSees, a default value for torsional stiffness was used (GJ). In versions 3.1.0 and newer fiber sections require a value for torsional stiffness. This is a 2D example with negligible torsion, however a value is required. The Young's Modulus is used for convenience.\nThe discretization can be visualized as such:\n.align-centeralign-center width=\u0026ldquo;400px\u0026rdquo;\nCross section of rectangular beam showing fiber discretization\nElements \u0026nbsp; dispBeamColumnThermal elements are used because temperature-dependent thermal and mechanical steel properties can be applied to these elements. Any portion of the structure that is being heated must use elements that are compatible with uniaxialMaterial Steel01Thermal. At the time this model was developed, dispBeamColumnThermal was the only element type that could have tempurature-dependent thermal and mechanical properties applied to them.\nThe beam is made of one element with 5 iteration points and connects nodes 1 \u0026amp; 2. OpenSees is sensitive to the number of iteration points in each element and this could change the result of the recorded displacement. For this reason, it is important to perform these benchmarking examples to establish how many iteration points allows for convergence to the expected recorded displacement. To code the number of iteration points, we use the following syntax:\ndispBeamColumnThermal eleTag iNode jNode numIntgrPts secTag TransfTag;\nElement 1\nelement dispBeamColumnThermal 1 1 2 5 $secTag $transftag;Element 2\nelement dispBeamColumnThermal 1 2 3 5 $secTag $transftag; Output Recorders \u0026nbsp; Displacement of the middle of node (2) in DOF 1 (horizontal direction) and the horizontal reaction force from the boundary conditions is what we want to record. To do so, a folder within your working directory must be created. dataDir is the command to create that folder and should be defined at the beginning of the model. This is where your output files will be saved.\nset dataDir Examples/EXAMPLE2_OUTPUT;file mkdir $dataDir;Displacement of the middle node (2) in DOF 1 (Horizontal Displacement)\nrecorder Node -file $dataDir/MidspanNodeDisp.out -time -node 2 -dof 1 disp;Recording reactions at the boundary conditions:\nrecorder Node -file $dataDir/BoundryRXN.out -time -node 1 3 -dof 1 2 reaction;Recording the section forces in Elements 1 \u0026amp; 2:\nrecorder Element -file $dataDir/ele_force_1.out -time -ele 1 section 2 forcerecorder Element -file $dataDir/ele_force_2.out -time -ele 2 section 2 forceLearn more about the Recorder Command: [Recorder Command \u0026lt;http://opensees.berkeley.edu/wiki/index.php/Recorder_Command\u0026gt;].title-ref __\nThermal Loading \u0026nbsp; This particular model is heating a beam to a set temperature over the time period of the model. We are not asking OpenSees to use a specific time-temperature curve, rather linearly ramp up the temperature from ambient to 1180 ° C.\nTherefore, we set the maximum temperature as follows:\nT = Max Tempurature degcelciusdeg celcius set T 1180;In OpenSees, the user can define 2 or 9 temperature data points through the cross section. In a 2D analysis framework, like this example, temperature data point locations are specified on the y-axis of the local coordinate system (as shown in the figure above). And are linearly interpolated between the defined points. Because this example is using a uniformly heated beam, the entire cross section is one temperature, and two temperature points on each extreme fiber on the y-axis will be chosen. The beam has a depth of 200mm, therefore, Y1 = 100 mm \u0026amp; Y2 = -100 mm for the top and bottom fibers respectively.\nLocation of bottom extreme fiber of beam mmmm set Y1 -100;Location of top extreme fiber of beam mmmm set Y2 100; .align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nLocation of defined input temperature locations on the member cross section\nThe bottom extreme fiber temperature must be defined first. The target maximum temperature for each extreme fiber is set to 1180 ° C and will be increased incrementally and linearly as the time step continues in the analysis. An external temperature data set can could also be used for more complex temperature loading.\nElement 1 will remain at ambient temperature 20 ° C, while Element 2 will be heated to the target tempurature. The syntax for this is:\npattern Plain 1 Linear eleLoad -ele 1 -type --beamThermal $T $Y2 $T Y1; eleLoad -ele 2 -type --beamThermal $T $Y2 $T Y1  Thermal Analysis \u0026nbsp; Thermal loading is applied in 1000 steps, with a load factor of 0.001. Each step is a 0.001 increment of the maximum temperature specified in the thermal loading step: T. The analysis is a static analysis and the contraints of the beam are plain. 1000 increments was also used during thermal analysis to allow for easy correlation between the input temperatures and the recorded output.\nA variety of load factors were examined and the solution converged when a load factor of 0.001 was used. OpenSees is sensitive to the load factor, therefore, it is important to ensure that benchmarking examples are performed to determine the proper load factor to use in structural fire engineering analyses.\nset Nsteps 1000set Factor \\[expr 1.0/$Nsteps\\];integrator LoadControl $Factor;analyze $Nsteps; Output Plots \u0026nbsp; After the model has completed running, the results will be a horizontal displacement of the recorded node, the internal forces in the elements, and the reactions from the boundary conditions. Since the temperature was linearly ramped up from ambient to 1180 ° C, the user can develop a temperature history that matches every increment of the model.\nElement 1 internal axial force vs. temperature\n.align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nNode 2 Horizontal displacement versus temperature\n.align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nSources \u0026nbsp; 11 European Committee for Standardization (CEN). (2005). Eurocode 3: Design of Steel Structures, Part 1.2: General Rules - Structural Fire Design."
      })
      .add(
      
      
      {
        id: 18,
        tag: "en",
        href: "/opensees-gallery/examples/thermalexamples/thermalexample3/",
        title: "Example 3",
        description: "A 6m long beam has a uniform applied load of 10 kN/m. With the loading sustained, the beam is heated to a target temperature of 1180 ° C.\n{.align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;}\n",
        
        
        content: "A 6m long beam has a uniform applied load of 10 kN/m. With the loading sustained, the beam is heated to a target temperature of 1180 ° C.\n.align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nElevation of beam and member cross-section\nExample overview: A steel beam is subjected to a uniform temperature using a linear time-temperature history. Vertical midspan displacement of the heated beam is recorded throughout the analysis. An investigation is performed on the impact the following parameters have on the midspan displacement of the beam: (i) including 2nd order geometric transformations, and (ii) restraining the horizontal displacement of the boundary conditions\nDownload Example 3 files:\nExample3.tcl\nWsectionThermal.tcl\nExample 3 Outputs \u0026lt;files/Example3_OUTPUT.zip\u0026gt;.interpreted-text role=\u0026ldquo;download\u0026rdquo;.\nObjectives \u0026nbsp; Develop a simply supported steel beam model using displacement-based beam elements with tempurature-dependent material properites, Record the midspan vertical displacment due to a linear time-temperature heating curve and a uniformly distributed gravity load, and Demonstrate the difference in midspan displacement of the beam when including 2nd order geometric transformations and restraining the beam against horizontal displacement of the beam ends. Material \u0026nbsp; The uniaxialMaterial Steel01Thermal includes temperature-dependent steel thermal and mechanical properties according to Eurocode 3 carbon steel. More details of Steel01 can be found at: Steel01 Material\u0026nbsp; uniaxialMaterial Steel01Thermal $matTag $Fy $Es $b;Es = 210000 MPa (Young\u0026rsquo;s modulus of elasticity at ambient temperatures)\nFy = 250 MPa (Yield strength of material at ambient temperatures)\nb = 0.01 (Strain-Hardening Ratio)\nTransformation \u0026nbsp; Both Linear \u0026amp; Corotational (Non-Linear)Transformations were used, and the resulting midspan displacements of the beams were recorded to view differences of including 2nd order bending effects.\ngeomTransf Linear $transftag; or\ngeomTransf Corotational $transftag; Learn more about geometric transofrmations: Geometric Transformation\u0026nbsp; section \u0026nbsp; This example uses a W-shape beam, therefore an external .tcl script is used to define the fiber sections. This script uses fibersecThermal to procure a fibered W-shape section with a section tag to be used while defining elements. Eight fibers are used throughout the web and four fibers within each flange.\nIn previous versions of OpenSees, a default value for torsional stiffness was used (GJ). In versions 3.1.0 and newer fiber sections require a value for torsional stiffness. This is a 2D example with negligible torsion, however a value is required. The Young's Modulus is used for convenience.\nWsection dimensions:\nset d 355; #mmset bf 171.5; #mmset tf 11.5; #mmset tw 7.4; #mmset nfdw 8; #mmset nftw 1; #mmset nfbf 1; #mmset nftf 4; #mm secTag - section tag matTag - material tag d = nominal depth tw = web thickness bf = flange width tf = flange thickness nfdw = number of fibers along web depth nftw = number of fibers along web thickness nfbf = number of fibers along flange width nftf = number of fibers along flange thickness Gj = torsional stiffness # WsectionThermal secTag matTag d bf tf tw nfdw nftw nfbf nftf Gj WsectionThermal 1 1 $d $bf $tf $tw 8 1 1 4 $Es .align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nCross section of W-shape showing fibers in the flanges and the web\nElement \u0026nbsp; dispBeamColumnThermal elements are used because temperature-dependent thermal and mechanical steel properties can be applied to these elements. Any portion of the structure that is being heated must use elements that are compatible with uniaxialMaterial Steel01Thermal. At the time this model was developed, dispBeamColumnThermal was the only element type that could have tempurature-dependent thermal and mechanical properties applied to them.\nThis example was developed using 6 elements along the length of the beam.\ndispBeamColumnThermal eleTageleTag iNode jNodejNode numIntgrPts secTagsecTag TransfTag;\nelement dispBeamColumnThermal $secTag 1 2 5 $secTag $transftag;This example will build off of the benchmarked examples and therefore used 5 iteration points in each element to simulate the beam bending and thermal expansion.\nOutput Recorders \u0026nbsp; dataDir is defined at the beginning of the model, this creates a folder within your working directory where output files will be saved.\nset dataDir Examples/EXAMPLE3_OUTPUT;file mkdir $dataDir;Displacement of the midspan node (4) in DOF 2 (Vertical Displacement)\nrecorder Node -file $dataDir/Midspan_Disp.out\\\u0026#34; -time -node 4 -dof 2 disp;Reaction forces at end nodes (nodes 1 \u0026amp; 7)\nrecorder Node -file $dataDir/RXNs.out -time -node 1 7 -dof 2 reaction;Learn more about the Recorder Command: Recorder Command\u0026nbsp; Thermal Loading \u0026nbsp; This particular model is heating a beam to a set temperature over the time period of the model. We are not asking OpenSees to use a specific time-temperature curve, rather linearly ramp up the temperature from ambient to 1180 ° C.\nTherefore, we set the maximum temperature as follows:\nset T 1180; # Max temperature, deg. celsiusIn OpenSees, the user can define 2 or 9 temperature data points through the cross section. In a 2D analysis framework, like this example, temperature data point locations are specified on the y-axis of the local coordinate system (as shown in the figure above). And are linearly interpolated between the defined points. Because this example is using a uniformly heated beam, two temperature points on each extreme fiber on the y-axis will be chosen. The beam has a depth of d, therefore, Y1 = d/2 \u0026amp; Y2 = -d/2 the top and bottom fibers respectively.\nTop fiber of beam\nset Y1 [expr $d/2];Bottom fiber of beam\nset Y2 [expr -$d/2]; .align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nLocation of defined input temperature locations on the member cross section\nThe bottom extreme fiber temperature must be defined first. The target maximum temperature for each extreme fiber is set to 1180 ° C and will be increased incrementally and linearly as the time step continues in the analysis. An external temperature data set could also be used for more complex temperature loading.\nUsing a plain linear loading pattern, Elements 1-6 will be heated to the target tempurature, T using a for loop for effecency. The syntax for this is:\npattern Plain 3 Linear for set level 1 $level \\\u0026lt;= 6 incr level 1 set eleID $level eleLoad -ele $eleID -type -beamThermal $T $Y2 $T $Y1; Thermal Analysis \u0026nbsp; Thermal loading is applied in 1000 steps, with a load factor of 0.001. Each step is a 0.001 increment of the maximum temperature specified in the thermal loading step: T. The analysis is a static analysis and the contraints of the beam are plain. 1000 increments was also used during thermal analysis to allow for easy correlation between the input temperatures and the recorded output.\nA variety of load factors were examined and the solution converged when a load factor of 0.001 was used. OpenSees is sensitive to the load factor, therefore, it is important to ensure that benchmarking examples are performed to determine the proper load factor to use in structural fire engineering analyses.\nset Nstep 1000;Thermal load is applied in 1000 steps. Each step is an 0.001 increment of the maximum temperature specified in the thermal loading step T (1180)\nset Factor \\[expr 1.0/$Nstep\\]; integrator LoadControl $Factor; analyze $Nstep; Output Plots \u0026nbsp; After the model has completed running, the results will be a vertical midspan displacement of the recorded node. Since the temperature was linearly ramped up from ambient to 1180 ° C, the user can develop a temperature history that matches every increment of the model. Additionally,mid-span displacement of the beam when including 2nd order geometric transformations, as well as restraining the horizontal boundary conditions are plotted. The same model was executed in the finite element software Abaqus additonally plotted as \u0026quot;AB\u0026quot;.\n.align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nSources \u0026nbsp; [1] W. Maddalozzo and E.C. Fischer, \u0026quot;Post-earthquake fire performance of steel buildings,\u0026quot; World Conference on Earthquake Engineering, 17WCEE, Sendai, Japan - September 13-18, 2020."
      })
      .add(
      
      
      {
        id: 19,
        tag: "en",
        href: "/opensees-gallery/examples/thermalexamples/thermalexample4/",
        title: "Example 4",
        description: "A 6 m x 3.5 m single bay frame with a 2 kN/m distributed load is subjected to a non-linear fire curve. \u0026nbsp; {.align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;}\n",
        
        
        content: "A 6 m x 3.5 m single bay frame with a 2 kN/m distributed load is subjected to a non-linear fire curve. \u0026nbsp; .align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nElevation of frame\nExample overview: A one-bay frame is considered with a uniformly distributed load (2 kN/m). The frame is exposed to a fire. Heat transfer analyses were performed using a commercially available finite element program to calculate the temperature distribution through the cross section,and the temperatures at each fiber when the members are exposed to a non-linear gas time-temperature curve. The horizontal displacements of the top corners of frame are restrained to represent lateral bracing, and the midspan displacement of the beam is recorded throughout the analysis.\nDownload Example 4 files:\nExample4.tcl\nWsectionThermal.tcl\nNodal Temperature Files \u0026lt;files/Ex4_NodalTemperatureFiles.zip\u0026gt;.interpreted-text role=\u0026ldquo;download\u0026rdquo;.\nExample 4 Outputs \u0026lt;files/Example4_OUTPUT.zip\u0026gt;.interpreted-text role=\u0026ldquo;download\u0026rdquo;.\nObjectives \u0026nbsp; Example 4 Objectives: 1. Develop a portal frame in OpenSees using displacement-based elements with tempurature-dependent material properties, and 2. Implementing user-defined time-tempurature histories for the elements calculated through heat transfer analysis.\nMaterial \u0026nbsp; The uniaxialMaterial Steel01Thermal includes temperature-dependent steel thermal and mechanical properties according to Eurocode 3 carbon steel. More details of Steel01 can be found at: Steel01 Material\u0026nbsp; uniaxialMaterial Steel01Thermal $matTag $Fy $Es $b;Es = 210000 MPa (Young\u0026rsquo;s modulus of elasticity at ambient temperatures)\nFy = 275 MPa (Yield strength of material at ambient temperatures)\nb = 0.01 (Strain-Hardening Ratio)\nTransformation \u0026nbsp; Because the beams in this example experience large deflections, 2nd order bending effects were considered using the Corotational geometric transformation.\ngeomTransf Corotational $transftag;Learn more about geometric transofrmations: Geometric Transformation\u0026nbsp; section \u0026nbsp; This example uses a W-shape beam, therefore an external .tcl script is used to define the fiber sections. This script uses fibersecThermal to procure a fibered W-shape section with a section tag to be used while defining elements. Eight fibers are used throughout the web and four fibers within each flange.\nIn previous versions of OpenSees, a default value for torsional stiffness was used (GJ). In versions 3.1.0 and newer fiber sections require a value for torsional stiffness. This is a 2D example with negligible torsion, however a value is required. The Young's Modulus is used for convenience.\nWsection dimensions:\nset secTag 1;set d 160;set bf 82;set tf 7.4;et tw 5.0;set nfdw 8;set nftw 1;set nfbf 1;set nftf 4; secTag - section tag matTag - material tag d = nominal depth tw = web thickness bf = flange width tf = flange thickness nfdw = number of fibers along web depth nftw = number of fibers along web thickness nfbf = number of fibers along flange width nftf = number of fibers along flange thickness Gj = torsional stiffness WsectionThermal secTag matTag d bf tf tw nfdw nftw nfbf nftf Gj\nWsectionThermal $secTag $matTag $d $bf $tf $tw 8 1 1 4 $Es .align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nCross section of W-shape showing fibers in the flanges and the web\nElement \u0026nbsp; dispBeamColumnThermal elements are used because temperature-dependent thermal and mechanical steel properties can be applied to these elements. Any portion of the structure that is being heated must use elements that are compatible with uniaxialMaterial Steel01Thermal. At the time this model was developed, dispBeamColumnThermal was the only element type that could have tempurature-dependent thermal and mechanical properties applied to them.\ndispBeamColumnThermal eleTageleTag iNode jNodejNode numIntgrPts secTagsecTag TransfTag;\nelement dispBeamColumnThermal 1 1 2 3 $secTag $transftag;Each column and beam element is created using ten displacement-based elements with 3 iteration points in each element.\nOutput Recorders \u0026nbsp; $dataDir is defined at the beginning of the model, this creates a folder within your working directory where output files will be saved. \u0026gt;set dataDir Examples/EXAMPLE4_OUTPUT;\nfile mkdir $dataDir;Displacement of the beam midspan node (27), DOF 2 (Vertical Displacement)\nrecorder Node -file $dataDir/Midspan_BeamDisp.out -time -node 27 -dof 2 disp;Reaction forces at end nodes. (1 \u0026amp; 12)\nrecorder Node -file $dataDir/RXNS.out -time -node 1 12 -dof 2 3 reaction;Learn more about the Recorder Command: Recorder Command\u0026nbsp; Thermal Loading \u0026nbsp; This particular model is heated using a fire time tempurature curve shown below. The fiber temperatures, or the temperature distribution through the cross section was calculated by performing a heat transfer analysis.\n.align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nThe results from the heat transfer analysis were used as inputs for the fiber temperatures in OpenSees. The locations of the input tempurature locations can be seen in the figure below.\nThree tempurature input files were created for the tempurature distribution of the beam and columns. Each tempurature file has 10 columns representing: Time, T1, T2, T3, T4, T5, T6, T7, T8 \u0026amp; T9. Time ranges from 0 to 1 to correlete with OpenSees analysis time steps. The T1 through T9 columns represent temperatures at each of the locations shown below for nine fibers through the cross section.\nThe red dots above below are locations where nodal temperatures were recorded during the heat transfer analysis and red dotted lines represent temperature input locations. The code below shows how to define each of the temperature input locations. The temperature through the depth of the web was constant. :\nset Y9 [expr -$d/2]; set Y2 [expr -($d/2 - 0.99*$tf)]; set Y3 [expr -($d/2 - $tf)]; set Y4 [expr -$d/4]; set Y5 0.0; set Y6 [expr $d/4]; set Y7 [expr ($d/2 - $tf)]; set Y8 [expr ($d/2 - 0.99*$tf)]; set Y9 [expr $d/2]; .align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nLocation of defined input temperature locations and extracted nodal temperatures on the member cross section (both beam and columns)\nThe bottom extreme fiber temperature must be defined first in the thermal load pattern. The input temperature files must be in your working directories or have their paths specified.\nTemperature loading for the beam\npattern Plain 11 Linear  for set level 21 $level \\\u0026lt;= 30 incr level 1 set eleID $level; eleLoad -ele $eleID -type -beamThermal -source BeamTemp.txt $Y9 $Y8 $Y7 $Y6 $Y5 $Y4 $Y3 $Y2 $Y1;Temperature loading for column 1\npattern Plain 11 Linear  for set level 1 $level \\\u0026lt;= 10 incr level 1 set eleID $level; eleLoad -ele $eleID -type -beamThermal -source Column1Temp.txt $Y9 $Y8 $Y7 $Y6 $Y5 $Y4 $Y3 $Y2 $Y1;Temperature loading for column 2\npattern Plain 11 Linear  for set level 11 $level \\\u0026lt;= 20 incr level 1 set eleID $level; eleLoad -ele $eleID -type -beamThermal -source Column2Temp.txt $Y$Y8 $Y7 $Y6 $Y5 $Y4 $Y3 $Y2 $Y1; Thermal Analysis \u0026nbsp; Thermal loading is applied in 1000 steps, with a load factor of 0.001. Each step is a 0.001 increment of the maximum temperature specified in the thermal loading step: T. The analysis is a static analysis and the contraints of the beam are plain. 1000 increments was also used during thermal analysis to allow for easy correlation between the input temperatures and the recorded output.\nA variety of load factors were examined and the solution converged when a load factor of 0.001 was used. OpenSees is sensitive to the load factor, therefore, it is important to ensure that benchmarking examples are performed to determine the proper load factor to use in structural fire engineering analyses.\nset Nstep 1000;set Factor \\[expr 1.0/$Nstep\\];integrator LoadControl $Factor;analyze $Nstep; Output Plots \u0026nbsp; After the model has completed running, the results will be the vertical midspan displacement of the beam. This displacement can be plotted against the time of the fire. It is suggested that if the user would like to develop a temperature history that matches every increment of the model, the same number of tempurature inputs as time steps is used.\nBeam midspan displacement versus time for the heated one-bay frame:\n.align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nSources \u0026nbsp; 11 European Committee for Standardization (CEN). (2005). Eurocode 3: Design of Steel Structures, Part 1.2: General Rules - Structural Fire Design.\n22 W. Maddalozzo and E.C. Fischer, \u0026quot;Post-earthquake fire performance of steel buildings,\u0026quot; World Conference on Earthquake Engineering, 17WCEE, Sendai, Japan - September 13-18, 2020."
      })
      .add(
      
      
      {
        id: 20,
        tag: "en",
        href: "/opensees-gallery/examples/example4/",
        title: "Example 4: Multibay Two Story Frame",
        description: "A multi-bay reinforced concrete frame is investigated.",
        
        
        content: "Example 4.1 \u0026nbsp; This example is of a reinforced concrete multibay two story frame, as shown in Figure 1, subject to gravity loads. The files for this example are: Python Tcl \u0026lt;a href=\u0026quot;Example4.py\u0026quot;\u0026gt;\u0026lt;code\u0026gt;Example4.py\u0026lt;/code\u0026gt;\u0026lt;/a\u0026gt;\u0026lt;/li\u0026gt; \u0026lt;a href=\u0026quot;Example4.tcl\u0026quot;\u0026gt;\u0026lt;code\u0026gt;Example4.tcl\u0026lt;/code\u0026gt;\u0026lt;/a\u0026gt;\u0026lt;/li\u0026gt; A model of the frame shown in Figure 1 is created. The number of objects in the model is dependent on the parameter numBay. The (numBay + 1)*3 nodes are created, one column line at a time, with the node at the base of the columns fixed in all directions. Three materials are constructed, one for the concrete core, one for the concrete cover and one for the reinforcement steel. Three fiber discretized sections are then built, one for the exterior columns, one for the interior columns and one for the girders. Each of the members in the frame is modelled using nonlinear beam-column elements with 4 (nP) integration points and a linear geometric transformation object.\n\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e For gravity loads, a single load pattern with a linear time series and two vertical nodal loads acting at the first and second floor nodes of each column line is used. The load at the lower level is twice that of the upper level and the load on the interior columns is twice that of the exterior columns.\nFor the lateral load analysis, a second load pattern with a linear time series is introduced after the gravity load analysis. Associated with this load pattern are two nodal loads acting on nodes 2 and 3, with the load level at node 3 twice that acting at node 2.\nThe integrator for the analysis will be LoadControl with a load step increment of 0.1. The constraints are enforced with a Plain constraint handler.\nOnce the components of the analysis have been defined, the analysis object is then created. For this problem a Static analysis is used and 10 steps are performed to load the model with the desired gravity load.\nAfter the gravity load analysis has been performed, the gravity loads are set to constant and the time in the domain is reset to 0.0. A new LoadControl integrator is now added. The new LoadControl integrator has an initial load step of 1.0, but this can vary between 0.02 and 2.0 depending on the number of iterations required to achieve convergence at each load step. 100 steps are then performed.\nThe output consists of the file Node41.out containing a line for each step of the lateral load analysis. Each line contains the load factor, the lateral displacements at nodes 2 and 3. A plot of the load-displacement curve for the frame is given in Figure 2.\n\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e"
      })
      .add(
      
      
      {
        id: 21,
        tag: "en",
        href: "/opensees-gallery/examples/thermalexamples/thermalexample5/",
        title: "Example 5",
        description: "A two-bay frame that measures 2.4 m x 1.18 m with a 60 N/m distributed load and column point loads is subjected to a fire in one of the bays. The heated bay is heated linearly to a target temperature of 550 ° C.\n{.align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;}\n",
        
        
        content: "A two-bay frame that measures 2.4 m x 1.18 m with a 60 N/m distributed load and column point loads is subjected to a fire in one of the bays. The heated bay is heated linearly to a target temperature of 550 ° C.\n.align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nElevation of two-bay frame\nExample overview: This example will combine the modeling methodologies developed through the other examples and apply them to a two-bay frame with a fire in one of the bays. Recorded data from the OpenSees analysis will be compared with the experimental test data 22 . Heat transfer analyses were performed using a commercially available finite element program to calculate the temperature distribution through the cross sections when the members are exposed to a linear gas time-temperature curve. Horizontal displacement of upper corners, U1 \u0026amp; U2 are recorded.\nDownload Example 5 files:\nExample5.tcl\nWsectionThermal.tcl\nExample 5 Outputs \u0026lt;files/Example5_OUTPUT.zip\u0026gt;.interpreted-text role=\u0026ldquo;download\u0026rdquo;.\nObjectives \u0026nbsp; Example 5 Objectives: 1. Create a two-bay frame in OpenSees using displacement-based elements with tempurature-dependent material properties, 2. Implementing user-defined time-tempurature histories for the elements calculated through heat transfer analysis, and 3. Compare recorded parameters from the OpenSees model to experimental testing data 22 to benchmark modeling methodologies.\nExperimental Test Overview\nA two-bay frame was tested by researchers 22 . Each bay size was 1.2 m in width and 1.18 m in height. Point loads were applied at the beam-column joints in the lateral and gravity directions in addition to a uniformly distributed load applied to the beams. The columns and beam of one of the bays was heated using electrical heaters that surrounded each of the members, therefore, uniformly heating each member (there was no thermal gradient through the cross section). The temperature was increased until failure.\nMaterial \u0026nbsp; The uniaxialMaterial Steel01Thermal includes temperature-dependent steel thermal and mechanical properties per Eurocode 3 11 . More details of Steel01 can be found at: Steel01 Material\u0026nbsp; Es = 210 GPa (Young\u0026rsquo;s modulus of elasticity at ambient temperatures) Fy = 355 MPa (Yield strength of material at ambient temperatures) b = 0.001 (Strain-Hardening Ratio) set matTag 1;uniaxialMaterial Steel01Thermal $matTag $Fy $Es $b; Transformation \u0026nbsp; Because the beams and columns in this example experience bending, 2nd order bending effects were considered using the Corotational geometric transformation.\ngeomTransf Corotational $transftag;Learn more about geometric transofrmations: Geometric Transformation\u0026nbsp; Section \u0026nbsp; This example uses an external .tcl script to define the cross section. This script uses fibersecThermal to procure a fibered W-shape section with a section tag to be used while defining elements. Eight fibers are used throughout the web and four fibers within each flange.\nIn previous versions of OpenSees, a default value for torsional stiffness was used (GJ). In versions 3.1.0 and newer fiber sections require a value for torsional stiffness. This is a 2D example with negligible torsion, however a value is required. The Young\u0026rsquo;s Modulus is used for convenience. Wsection dimensions are (units are meters):\nset secTag 1; # section Tag set d 0.08; # depth of beam set bf 0.046; # flange width set tf 0.0052; # flange thickness set tw 0.0038; # web thickness secTag - section tag matTag - material tag d = nominal depth tw = web thickness bf = flange width tf = flange thickness nfdw = number of fibers along web depth nftw = number of fibers along web thickness nfbf = number of fibers along flange width nftf = number of fibers along flange thickness Gj = torsional stiffness # WsectionThermal secTag matTag d bf tf tw nfdw nftw nfbf nftf Gj WsectionThermal $secTag $matTag $d $bf $tf $tw 8 1 1 4 $Es .align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nCross section of W-shape showing fibers in the flanges and the web\nElement \u0026nbsp; dispBeamColumnThermal elements are used because temperature-dependent thermal and mechanical steel properties can be applied to these elements. Any portion of the structure that is being heated must use elements that are compatible with uniaxialMaterial Steel01Thermal. At the time this model was developed, dispBeamColumnThermal was the only element type that could have tempurature-dependent thermal and mechanical properties applied to them.\n# $eleTag $iNode $jNode $numIntgrPts $secTag $TransfTag; element dispBeamColumnThermal 1 1 2 3 $secTag $transftag;Each column and beam element is created using ten displacement-based elements with 3 iteration points in each element.\nOutput Recorders \u0026nbsp; dataDir is defined at the beginning of the model, this creates a folder within your working directory where output files will be saved.\nset dataDir Examples/EXAMPLE5_OUTPUT;file mkdir $dataDir;displacements of node U1 (node 11, top left), DOF 1 (Horizontal Displacement)\nrecorder Node -file $dataDir/Midspan_BeamDisp.out -time -node 11 -dof 1 disp;displacements of node U2 (node 22, top-middle), DOF 1 (Horizontal Displacement)\nrecorder Node -file $dataDir/Midspan_BeamDisp.out -time -node 22 -dof 1 disp;Reaction forces at support nodes (1, 12 and 23):\nrecorder Node -file $dataDir/RXNS.out -time -node 1 12 23 -dof 2 3 reaction;Learn more about the Recorder Command: Recorder Command\u0026nbsp; Thermal Loading \u0026nbsp; In this model, the beams and columns of the left bay are heated by increasing the temperature linearly from ambient temperature until failure. The right bay remains at ambient tempurature.\nTherefore, we set the maximum temperature as follows:\nset T 550; # Max Temperature, deg CIn OpenSees, the user can define 2 or 9 temperature data points through the cross section. In a 2D analysis framework, like this example, temperature data point locations are specified on the y-axis of the local coordinate system (as shown in the figure above). And are linearly interpolated between the defined points. Because this example is using a uniformly heated beam, two temperature points on each extreme fiber on the y-axis will be chosen. The beam has a depth of d, therefore, Y1 = d/2 and Y2 = -d/2 the top and bottom fibers respectively.\nTop fiber of beam\nset Y1 [expr $d/2];Bottom fiber of beam\nset Y2 [expr -$d/2];Location of defined input temperature locations on the member cross section (both beam and columns)\n.align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nThe bottom extreme fiber temperature must be defined first. The target maximum temperature for each extreme fiber is set to 550 ° C and will be increased linearly and incrementally as the time step continues in the analysis. An external temperature data set can could also be used for more complex temperature loading.\nUsing a for-loop and a plain linear loading pattern, elements 1-20 \u0026amp; 31-40 will be subjected to tempurature, T. These elements define the heated bay.\npattern Plain 2 Linear  for set i 1 $i \\\u0026lt;= 20 incr i  eleLoad -ele $i -type -beamThermal $T $Y2 $T $Y1;  for set i 31 $i \\\u0026lt;= 40 incr i eleLoad -ele $i -type -beamThermal $T $Y2 $T $Y1;; Thermal Analysis \u0026nbsp; Thermal loading is applied in 1000 steps, with a load factor of 0.001. Each step is a 0.001 increment of the maximum temperature specified in the thermal loading step: T. The analysis is a static analysis and the contraints of the beam are plain. 1000 increments was also used during thermal analysis to allow for easy correlation between the input temperatures and the recorded output. Each step is an 0.001 increment of the maximum temperature specified in the thermal loading step: T.\nA variety of load factors were examined and the solution converged when a load factor of 0.001 was used. OpenSees is sensitive to the load factor, therefore, it is important to ensure that benchmarking examples are performed to determine the proper load factor to use in structural fire engineering analyses.\nset Nstep 1000 set Factor \\[expr 1.0/$Nstep\\]; integrator LoadControl $Factor; analyze $Nstep; Output Plots \u0026nbsp; After the model has completed running, the results will be horizontal displacements of the recorded node. Since the temperature was linearly ramped up from ambient to 550 ° C, the user can develop a temperature history that matches every increment of the model. The displacements are benchmarked against test data 22 as shown in the figure below.\nNode U1 horizontal displacement versus temperature compared with the testing data\n.align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nNode U2 horizontal displacement versus temperature compared with the testing data\n.align-centeralign-center width=\u0026ldquo;500px\u0026rdquo;\nSources \u0026nbsp; 11 European Committee for Standardization (CEN). (2005). Eurocode 3: Design of Steel Structures, Part 1.2: General Rules - Structural Fire Design.\n22 Rubert A, Schaumann P. (1986). \u0026ldquo;Structural steel and plane frame assemblies under ﬁre action.\u0026rdquo; Fire Safety Journal, vol. 10, pp.173\u0026ndash;184."
      })
      .add(
      
      
      {
        id: 22,
        tag: "en",
        href: "/opensees-gallery/docs/library/frame/",
        title: "Frame",
        description: "Frame elements.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 23,
        tag: "en",
        href: "/opensees-gallery/examples/example5/",
        title: "Frame with Diaphragms",
        description: "A three-dimensional reinforced concrete rigid frame, is subjected to bi-directional earthquake ground motion.",
        
        
        content: "A three-dimensional reinforced concrete rigid frame, is subjected to bi-directional earthquake ground motion.\nExample5.tcl RCsection.tcl Or for Python:\nExample5.py render.py In both cases, the following ground motion records are required:\ntabasFN.txt tabasFP.txt Modeling \u0026nbsp; A model of the rigid frame shown in the figure below is created. The model consists of three stories and one bay in each direction. Rigid diaphragm multi-point constraints are used to enforce the rigid in-plane stiffness assumption for the floors. Gravity loads are applied to the structure and the 1978 Tabas acceleration records are the uniform earthquake excitations.\nNonlinear beam column elements are used for all members in the structure. The beam sections are elastic while the column sections are discretized by fibers of concrete and steel. Elastic beam column elements may have been used for the beam members; but, it is useful to see that section models other than fiber sections may be used in the nonlinear beam column element.\n\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e Analysis \u0026nbsp; A solution Algorithm of type Newton is used for the nonlinear problem. The solution algorithm uses a ConvergenceTest which tests convergence on the norm of the energy increment vector. The integrator for this analysis will be of type Newmark with a γ\\gamma of 0.25 and a β\\beta of 0.5. Due to the presence of the multi-point constraints, a Transformation constraint handler is used.\nOnce all the components of an analysis are defined, the Analysis itself is defined. For this problem a Transient analysis is used. 2000 steps are performed with a time step of 0.01.\nPost-Processing \u0026nbsp; The nodal displacements at nodes 9, 14, and 19 (the retained nodes for the rigid diaphragms) will be stored in the file node51.out for post-processing.\nThe results consist of the file node.out, which contains a line for every time step. Each line contains the time and the horizontal and vertical displacements at the diaphragm retained nodes (9, 14 and 19) i.e. time Dx9 Dy9 Dx14 Dy14 Dx19 Dy19. The horizontal displacement time history of the first floor diaphragm node 9 is shown in the figure below. Notice the increase in period after about 10 seconds of earthquake excitation, when the large pulse in the ground motion propogates through the structure. The displacement profile over the three stories shows a soft-story mechanism has formed in the first floor columns. The numerical solution converges even though the drift is ≈20%\\approx 20 \\% . The inclusion of P−ΔP-\\Delta effects shows structural collapse under such large drifts.\n\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e"
      })
      .add(
      
      
      {
        id: 24,
        tag: "en",
        href: "/opensees-gallery/examples/viscousdamper/",
        title: "Frame with Viscous Dampers",
        description: "This example demonstrates how to use the viscous damper material within a simple single story shear frame.",
        
        
        content: "This example demonstrates how to use the viscous damper material within a simple single story shear frame.\nThe files needed to analyze this structure in OpenSees are included here:\nThe main file: Supporting files\nTakY.th - uses the JR Takatori record from the Kobe 1995 earthquake (available in the zip file below) All files are available in a compressed format here: Viscous_Damper_Example.zip\nThe rest of this example describes the model and shows the analysis results.\nModel Description \u0026nbsp; Figure 1. Schematic representation of a viscous damper installed in the single story moment resisting frame. The viscous damper is modeled with a Two Node Link Element. This element follows a Viscous damper hysteretic response. An idealized schematic of the model is presented in Figure 1.\nThe units of the model are mm, kN, and seconds.\nBasic Geometry \u0026nbsp; The single bay single story frame shown in Figure 1 has 5000mm bay width and 3000mm story height (centerline). The period of the system is 0.7sec. Columns and beams of the frame are modeled with elastic beam-column elements.\nDamper Links \u0026nbsp; A Two Node Link Element is used to link the two nodes that define the geometry of the viscous damper.\nConstraints \u0026nbsp; the Nodes at the base of the frame are fixed. The beam (element 3 in Figure 1) is considered to be rigid.\nViscous Damper Material \u0026nbsp; To model the viscous damper the ViscousDamper is used. The input parameters that are selected for the damper example are as follows: Axial Stiffness K = 25 kN/mm, Damping Coefficient Cd=20.74 kN(s/mm)\u0026lt;sup\u0026gt;0.35\u0026lt;/sup\u0026gt; and exponent a=0.35.\nLoading \u0026nbsp; The single story frame with viscous damper is subjected to the 50% JR Takatori record from the Kobe 1995 earthquake in Japan.\nRecorders \u0026nbsp; The recorders used in this example include:\nThe Element recorder to track the damper axial force and axial displacement. The Node recorder to track the Frame displacement history at its roof. Analysis \u0026nbsp; A uniform excitation option is selected with application of ground acceleration history as the imposed motion. The Newmark integration scheme is selected for integration of the equations of motion with a time step dt = 0.001sec. Two percent mass proportional damping is used.\nResults \u0026nbsp; Simulation Results for the 50% JR Takatori Record \u0026nbsp; Figure 2. Displacement history at the roof of the single story MRF The force - displacement relationship from the viscous damper are shown in Figure 3. A comparison with results from a SAP2000 model is also shown in Figure 3. Results are nearly identical between the two models. Figure 3. Force - displacement relationship of the viscous damper and comparison with identical model in SAP2000 Example posted by: Sarven Akcelyan\u0026nbsp; and Prof. Dimitrios G. Lignos\u0026nbsp; (McGill University)"
      })
      .add(
      
      
      {
        id: 25,
        tag: "en",
        href: "/opensees-gallery/docs/advanced-settings/icons/",
        title: "Icons",
        description: "Configure secure access to icons from Bootstrap and Font Awesome.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 26,
        tag: "en",
        href: "/opensees-gallery/examples/cantilevertransient/",
        title: "Inelastic Cantilever",
        description: "A plane cantilever column is shaken by an earthquake. Material nonlinearity is accounted for using the force formulation and fiber-discretized cross sections",
        
        
        content: "In order to execute this notebook, go to the menu bar and click Run/Run all cells. You can also run individual cells by selecting the cell (a blue bar will appear to the left of the active cell, then pressing Shift+Enter.\nNOTE Before running this notebook, you must install the external dependencies. To to this, uncomment the following cell by removing the leading # character, execute the cell, then put the # character back to prevent it from running again, thereby \u0026ldquo;commenting it out\u0026rdquo;. Once everything is installed you may re-run the commented-out cell to hide the text generated by the installation.\n# !pip install -Ur requirements.txt# Linear algebra library import numpy as np # Plotting library import matplotlib.pyplot as plt # The next two lines set reasonable plot style defaults import scienceplots plt.style.use(\u0026#39;science\u0026#39;)## Configure units # Units are based on inch-kip-seconds import opensees.units.iks as units pi = units.pi; ft = units.ft; ksi = units.ksi; inch = units.inch;## Distributed Inelasticity 2d Beam-Column Element # fiber sectionSet up basic model geometry\n# import the openseespy interface which contains the \u0026#34;Model\u0026#34; class import opensees.openseespy as ops# generate Model data structure model = ops.Model(ndm=2, ndf=3) # Length of cantilever column L = 8*ft; # specify node coordinates model.node(1, 0, 0 ); # first node model.node(2, 0, L ); # second node # boundary conditions model.fix(1, 1, 1, 1 ) ## specify mass model.mass(2, 2.0, 1e-8, 1e-8)## Element name: 2d nonlinear frame element with distributed inelasticity # Create material and add to Model mat_tag = 1 # identifier that will be assigned to the new material E = 29000*ksi fy = 60*ksi Hkin = 0 Hiso = 0 model.uniaxialMaterial(\u0026#34;Steel01\u0026#34;, mat_tag, fy, E, 0.01) # model.uniaxialMaterial(\u0026#34;ElasticPP\u0026#34;, mat_tag, E, fy/E) # model.uniaxialMaterial(\u0026#34;UniaxialJ2Plasticity\u0026#34;, mat_tag, E, fy, Hkin, Hiso) Create a section \u0026nbsp; import opensees.section # Load cross section geometry and add to Model sec_tag = 1 # identifier that will be assigned to the new section SecData =  SecData[\u0026#34;nft\u0026#34;] = 4 # no of layers in flange SecData[\u0026#34;nwl\u0026#34;] = 8 # no of layers in web SecData[\u0026#34;IntTyp\u0026#34;] = \u0026#34;Midpoint\u0026#34;; SecData[\u0026#34;FlgOpt\u0026#34;] = True section = opensees.section.from_aisc(\u0026#34;Fiber\u0026#34;, \u0026#34;W24x131\u0026#34;, # \u0026#34;W14x426\u0026#34;, sec_tag, tag=mat_tag, mesh=SecData, ndm=2, units=units)import sees.section sees.section.render(section);Output:\n\u0026lt;Figure size 350x262.5 with 1 Axes\u0026gt;Printing the fiber section will display the effective cross-sectional properties which result from quadrature over the cross section fibers:\nprint(section)Output:\nSectionGeometry area: 38.42890000000003 ixc: 4013.509824163335 iyc: 343.8869259102087 Create an element \u0026nbsp; cmd = opensees.tcl.dumps(section, skip_int_refs=True) model.eval(cmd) # Create element integration scheme nIP = 4 int_tag = 1 model.beamIntegration(\u0026#34;Lobatto\u0026#34;, int_tag, sec_tag, nIP) # Create element geometric transformation model.geomTransf(\u0026#34;Linear\u0026#34;, 1) # Finally, create the element # CONN Geom Int model.element(\u0026#34;ForceBeamColumn\u0026#34;, 1, (1, 2), 1, int_tag) Analysis \u0026nbsp; Eigenvalue Analysis \u0026nbsp; # State = Initialize_State (Model,ElemData) # State = Structure(\u0026#39;stif\u0026#39;,Model,ElemData,State) # Initialize the analysis state for transient analysis model.analysis(\u0026#34;Transient\u0026#34;) # Form stiffness and mass matrices Kf = model.getTangent(k=1.0) # free DOF stiffness matrix Kf for initial State Mf = model.getTangent(m=1.0) # free DOF mass matrix Ml print(\u0026#34;Kf:\u0026#34;, Kf, sep=\u0026#34;\\n\u0026#34;) print(\u0026#34;Mf:\u0026#34;, Mf, sep=\u0026#34;\\n\u0026#34;)Output:\nKf: [[ 1.57505061e+03 0.00000000e+00 7.56024291e+04] [ 0.00000000e+00 1.16087302e+04 -1.21265960e-12] [ 7.56024291e+04 -1.21265960e-12 4.83855547e+06]] Mf: [[2.e+00 0.e+00 0.e+00] [0.e+00 1.e-08 0.e+00] [0.e+00 0.e+00 1.e-08]]Solve dynamic eigenvalue problem with scipy function eig\nimport scipy.linalg omega,Ueig = scipy.linalg.eig(Kf,Mf) # echo eigenmode periods print(\u0026#39; The three lowest eigenmode periods are\u0026#39;) T = 2*pi/np.sqrt(omega) print(T)Output:\nThe three lowest eigenmode periods are [4.47793313e-01+0.j 2.85641961e-07+0.j 5.83159707e-06+0.j]In general the eigen function should be used, which takes advantage of sparsity in the system\nfor w in model.eigen(2): print(2*pi/np.sqrt(w))Output:\n0.44779331340120765 5.8315970735940395e-06 Configure ground motion \u0026nbsp; # Apply damping in the first mode zeta = 0.02 model.modalDamping(zeta) # alphaM, betaK = 0.01, 0.01 # model.rayleigh(alphaM, betaK, 0, 0) # State = Add_Damping2State(\u0026#39;Modal\u0026#39;,Model,State,zeta)# Deltat = 0.02 # AccHst = np.loadtxt(\u0026#34;tabasFN.txt\u0026#34;) import quakeio Event = quakeio.read(\u0026#34;TAK000.AT2\u0026#34;) AccHst = Event.data Deltat = Event[\u0026#34;time_step\u0026#34;]load_tag = 1 model.timeSeries(\u0026#39;Path\u0026#39;, load_tag, dt=Deltat, factor=1.0, values=units.gravity*AccHst) model.pattern(\u0026#39;UniformExcitation\u0026#39;, 1, 1, accel=load_tag) Configure integration method \u0026nbsp; ## initialize data for solution strategy # gam bet model.integrator(\u0026#34;Newmark\u0026#34;, 1/2, 1/4, form=\u0026#34;d\u0026#34;) Perform integration \u0026nbsp; nt = len(AccHst) Uplt = np.zeros(nt) Vplt = np.zeros(nt) Aplt = np.zeros(nt) Pplt = np.zeros(nt) # Defo = zeros(np,1) # Forc = zeros(np,1) for k in range(nt): if model.analyze(1, Deltat) != 0: print(\u0026#34;Analysis failed\u0026#34;) break # extract values for plotting from response history Uplt[k] = model.nodeDisp (2, 1) Vplt[k] = model.nodeVel (2, 1) Aplt[k] = model.nodeAccel(2, 1) # Pplt[k] = Post[k].Pr[Pdof,:]; # Defo(k) = Post(k).Elem1.v; # Forc(k) = Post(k).Elem1.q; Post-processing \u0026nbsp; Displacement History \u0026nbsp; t = np.arange(nt)*Deltat; Xp = t Yp = (Uplt/L)*100 FigHndl, AxHndl = plt.subplots() AxHndl.set_xlabel(\u0026#39;Time (sec)\u0026#39;) AxHndl.set_ylabel(\u0026#39;Drift in X (\\\\%)\u0026#39;) AxHndl.plot(Xp,Yp,\u0026#39;b\u0026#39;) FigHndl.savefig(\u0026#34;drift.png\u0026#34;)Output:\n\u0026lt;Figure size 350x262.5 with 1 Axes\u0026gt; Shear force-displacement history \u0026nbsp; Xp = (Uplt/L)*100 Yp = Pplt FigHndl, AxHndl = plt.subplots() AxHndl.set_xlabel(\u0026#39;Lateral Drift (\\#)\u0026#39;) AxHndl.set_ylabel(\u0026#39;Lateral Force $P$\u0026#39;) AxHndl.plot(Xp, Yp, \u0026#39;b\u0026#39;) plt.show()Output:\n\u0026lt;Figure size 350x262.5 with 1 Axes\u0026gt;"
      })
      .add(
      
      
      {
        id: 27,
        tag: "en",
        href: "/opensees-gallery/examples/example3/",
        title: "Inelastic Plane Frame",
        description: "Nonlinear analysis of a concrete portal frame.",
        
        
        content: "\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e This set of examples investigates the nonlinear analysis of a reinforced concrete frame. The nonlinear beam column element with a fiber discretization of the cross section is used in the model. The files for this example are: Python Tcl \u0026lt;a href=\u0026quot;portal.py\u0026quot;\u0026gt;\u0026lt;code\u0026gt;portal.py\u0026lt;/code\u0026gt;\u0026lt;/a\u0026gt;\u0026lt;/p\u0026gt; \u0026lt;a href=\u0026quot;portal.tcl\u0026quot;\u0026gt;\u0026lt;code\u0026gt;portal.tcl\u0026lt;/code\u0026gt;\u0026lt;/a\u0026gt;\u0026lt;/p\u0026gt; These files define the following functions:\nFunction Description create_portal Creates a model of a portal frame gravity_analysis Performs a gravity analysis on a model pushover_analysis Performs a pushover analysis on a model transient_analysis Performs a transient analysis on a model create_portal \u0026nbsp; The function create_portal creates a model representing the portal frame in the figure above. The model consists of four nodes, two nonlinear beam-column elements modeling the columns and an elastic beam element to model the girder. For the column elements a section, identical to the section used in Example 2, is created using steel and concrete fibers.\nBegin with nodes and boundary conditions Python Tcl # create ModelBuilder (with two-dimensions and 3 DOF/node) model = ops.Model(ndm=2, ndf=3) # Create nodes # ------------ # create nodes \u0026amp; add to Domain - command: node nodeId xCrd yCrd model.node(1, 0.0, 0.0) model.node(2, width, 0.0) model.node(3, 0.0, height) model.node(4, width, height) # set the boundary conditions - command: fix nodeID uxRestrnt? uyRestrnt? rzRestrnt? model.fix(1, 1, 1, 1) model.fix(2, 1, 1, 1) set width 360 set height 144 model basic -ndm 2 -ndf 3 # Create nodes # tag X Y node 1 0.0 0.0 node 2 $width 0.0 node 3 0.0 $height node 4 $width $height # Fix supports at base of columns # tag DX DY RZ fix 1 1 1 1 fix 2 1 1 1 Next define the materials\nPython Tcl # Define materials for nonlinear columns # ------------------------------------------ # CONCRETE tag f\u0026#39;c ec0 f\u0026#39;cu ecu # Core concrete (confined) model.uniaxialMaterial(\u0026#34;Concrete01\u0026#34;, 1, -6.0, -0.004, -5.0, -0.014) # Cover concrete (unconfined) model.uniaxialMaterial(\u0026#34;Concrete01\u0026#34;, 2, -5.0, -0.002, -0.0, -0.006) # STEEL # Reinforcing steel fy = 60.0; # Yield stress E = 30000.0; # Young\u0026#39;s modulus # tag fy E b model.uniaxialMaterial(\u0026#34;Steel01\u0026#34;, 3, fy, E, 0.01) # Define materials for nonlinear columns # ------------------------------------------ # CONCRETE tag f\u0026#39;c ec0 f\u0026#39;cu ecu # Core concrete (confined) uniaxialMaterial Concrete01 1 -6.0 -0.004 -5.0 -0.014 # Cover concrete (unconfined) uniaxialMaterial Concrete01 2 -5.0 -0.002 0.0 -0.006 # STEEL # Reinforcing steel set fy 60.0; # Yield stress set E 30000.0; # Young\u0026#39;s modulus # tag fy E0 b uniaxialMaterial Steel01 3 $fy $E 0.01 Define a cross section for the columns Python Tcl # Define cross-section for nonlinear columns # ------------------------------------------ # set some parameters colWidth = 15.0 colDepth = 24.0 cover = 1.5 As = 0.6 # area of no. 7 bars # some variables derived from the parameters y1 = colDepth/2.0 z1 = colWidth/2.0 model.section(\u0026#34;Fiber\u0026#34;, 1) # Add the concrete core fibers model.patch(\u0026#34;rect\u0026#34;, 1, 10, 1, cover-y1, cover-z1, y1-cover, z1-cover, section=1) # Add the concrete cover fibers (top, bottom, left, right) model.patch(\u0026#34;rect\u0026#34;, 2, 10, 1, -y1, z1-cover, y1, z1, section=1) model.patch(\u0026#34;rect\u0026#34;, 2, 10, 1, -y1, -z1, y1, cover-z1, section=1) model.patch(\u0026#34;rect\u0026#34;, 2, 2, 1, -y1, cover-z1, cover-y1, z1-cover, section=1) model.patch(\u0026#34;rect\u0026#34;, 2, 2, 1, y1-cover, cover-z1, y1, z1-cover, section=1) # Add the reinforcing fibers (left, middle, right, section=1) model.layer(\u0026#34;straight\u0026#34;, 3, 3, As, y1-cover, z1-cover, y1-cover, cover-z1, section=1) model.layer(\u0026#34;straight\u0026#34;, 3, 2, As, 0.0, z1-cover, 0.0, cover-z1, section=1) model.layer(\u0026#34;straight\u0026#34;, 3, 3, As, cover-y1, z1-cover, cover-y1, cover-z1, section=1) # Define cross-section for nonlinear columns # ------------------------------------------ # set some parameters set colWidth 15 set colDepth 24 set cover 1.5 set As 0.60; # area of no. 7 bars # some variables derived from the parameters set y1 [expr $colDepth/2.0] set z1 [expr $colWidth/2.0] section Fiber 1  # Add the concrete core fibers patch rect 1 10 1 [expr $cover-$y1] [expr $cover-$z1] [expr $y1-$cover] [expr $z1-$cover] # Add the concrete cover fibers (top, bottom, left, right) patch rect 2 10 1 [expr -$y1] [expr $z1-$cover] $y1 $z1 patch rect 2 10 1 [expr -$y1] [expr -$z1] $y1 [expr $cover-$z1] patch rect 2 2 1 [expr -$y1] [expr $cover-$z1] [expr $cover-$y1] [expr $z1-$cover] patch rect 2 2 1 [expr $y1-$cover] [expr $cover-$z1] $y1 [expr $z1-$cover] # Add the reinforcing fibers (left, middle, right) layer straight 3 3 $As [expr $y1-$cover] [expr $z1-$cover] [expr $y1-$cover] [expr $cover-$z1] layer straight 3 2 $As 0.0 [expr $z1-$cover] 0.0 [expr $cover-$z1] layer straight 3 3 $As [expr $cover-$y1] [expr $z1-$cover] [expr $cover-$y1] [expr $cover-$z1]  gravity_analysis \u0026nbsp; We now implement a function called gravity_analysis which takes the instance of Model returned by create_portal, and proceeds to impose gravity loads and perform a static analysis. Its use will look like:\nPython Tcl # Create the model model = create_portal() # perform analysis under gravity loads status = gravity_analysis(model) create_portal; gravity_analysis; A single load pattern with a linear time series is created with two vertical nodal loads acting at nodes 3 and 4:\nPython Tcl model.pattern(\u0026#34;Plain\u0026#34;, 1, \u0026#34;Linear\u0026#34;, loads= # nodeID xForce yForce zMoment 3: [ 0.0, -P, 0.0], 4: [ 0.0, -P, 0.0] ) The model contains material non-linearities, so a solution algorithm of type Newton is used. The solution algorithm uses a ConvergenceTest which tests convergence of the equilibrium solution with the norm of the displacement increment vector. For this nonlinear problem, the gravity loads are applied incrementally until the full load is applied. To achieve this, a LoadControl integrator which advances the solution with an increment of 0.1 at each load step is used. The equations are formed using a banded storage scheme, so the System is BandGeneral. The equations are numbered using an RCM (reverse Cuthill-McKee) numberer. The constraints are enforced with a Plain constraint handler.\nOnce all the components of an analysis are defined, the Analysis object itself is created. For this problem a Static Analysis object is used. To achieve the full gravity load, 10 load steps are performed.\nAt end of analysis, the state at nodes 3 and 4 is output. The state of element 1 is also output.\nFor the two nodes, displacements and loads are given. For the beam-column elements, the element end forces in the local system are provided.\nThe nodeGravity.out file contains ten lines, each line containing 7 entries. The first entry is time in the domain at end of the load step. The next 3 entries are the displacements at node 3, and the final 3 entries the displacements at node 4.\npushover_analysis \u0026nbsp; In this example the nonlinear reinforced concrete portal frame which has undergone the gravity load analysis of Example 3.1 is now subjected to a pushover analysis.\nAfter performing the gravity load analysis on the model, the time in the domain is reset to 0.0 and the current value of all loads acting are held constant. A new load pattern with a linear time series and horizontal loads acting at nodes 3 and 4 is then added to the model.\nThe static analysis used to perform the gravity load analysis is modified to take a new DisplacementControl integrator. At each new step in the analysis the integrator will determine the load increment necessary to increment the horizontal displacement at node 3 by 0.1 in. 60 analysis steps are performed in this new analysis.\nFor this analysis the nodal displacements at nodes 3 and 4 will be stored in the file nodePushover.out for post-processing. In addition, the end forces in the local coordinate system for elements 1 and 2 will be stored in the file elePushover.out. At the end of the analysis, the state of node 3 is printed to the screen.\nIn addition to what is displayed on the screen, the file node32.out and ele32.out have been created by the script. Each line of node32.out contains the time, DX, DY and RZ for node 3 and DX, DY and RZ for node 4 at the end of an iteration. Each line of eleForce.out contains the time, and the element end forces in the local coordinate system. A plot of the load-displacement relationship at node 3 is shown in the figure below.\n\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e transient_analysis \u0026nbsp; The concrete frame which has undergone the gravity load analysis of Example 3.1 is now subjected to a uniform earthquake excitation.\nAfter performing the gravity load analysis, the time in the domain is reset to 0.0 and the time series for all active loads is set to constant. This prevents the gravity load from being scaled with each step of the dynamic analysis.\nPython Tcl model.loadConst(time=0.0) loadConst -time 0.0 Mass terms are added to nodes 3 and 4. A new uniform excitation load pattern is created. The excitation acts in the horizontal direction and reads the acceleration record and time interval from the file ARL360.g3. The file ARL360.g3 is created from the PEER Strong Motion Database ( http://peer.berkeley.edu/smcat/\u0026nbsp; ) record ARL360.at2 using the Tcl procedure ReadSMDFile contained in the file ReadSMDFile.tcl.\nThe static analysis object and its components are first deleted so that a new transient analysis object can be created.\nA new solution Algorithm of type Newton is then created. The solution algorithm uses a ConvergenceTest which tests convergence on the norm of the displacement increment vector. The integrator for this analysis will be of type Newmark with a γ=0.25\\gamma = 0.25 and β=0.5\\beta = 0.5 .\nThe integrator will add some stiffness proportional damping to the system, the damping term will be based on the last committed stifness of the elements, i.e. C=acKcommitC = a_c K_\\textcommit with ac=0.000625a_c = 0.000625 .\nThe equations are formed using a banded storage scheme, so the System is BandGeneral. The equations are numbered using an RCM (reverse Cuthill-McKee) numberer. The constraints are enforced with a Plain constraint handler.\nOnce all the components of an analysis are defined, the Analysis object itself is created. For this problem a Transient Analysis object is used. 2000 time steps are performed with a time step of 0.01.\nIn addition to the transient analysis, two eigenvalue analysis are performed on the model. The first is performed after the gravity analysis and the second after the transient analysis.\nFor this analysis the nodal displacenments at Nodes 3 and 4 will be stored in the file nodeTransient.out for post-processing. In addition the section forces and deformations for the section at the base of column 1 will also be stored in two seperate files. The results of the eigenvalue analysis will be displayed on the screen.\nGravity load analysis completed eigen values at start of transient: 2.695422e+02 1.750711e+04 Transient analysis completed SUCCESSFULLY eigen values at start of transient: 1.578616e+02 1.658481e+04 Node: 3 Coordinates : 0 144 commitDisps: -0.0464287 -0.0246641 0.000196066 Velocities : -0.733071 1.86329e-05 0.00467983 commitAccels: -9.13525 0.277302 38.2972 unbalanced Load: -3.9475 -180 0 Mass : 0.465839 0 0 0 0.465839 0 0 0 0 Eigenvectors: -1.03587 -0.0482103 -0.00179081 0.00612275 0.00663473 3.21404e-05 The two eigenvalues for the eigenvalue analysis are printed to the screen. The state of node 3 at the end of the analysis is also printed. The information contains the last committed displacements, velocities and accelerations at the node, the unbalanced nodal forces and the nodal masses. In addition, the eigenvector components of the eigenvector pertaining to the node 3 is also displayed.\nIn addition to the contents displayed on the screen, three files have been created. Each line of nodeTransient.out contains the domain time, and DX, DY and RZ for node 3. Plotting the first and second columns of this file the lateral displacement versus time for node 3 can be obtained as shown in the figure below. Each line of the files ele1secForce.out and ele1secDef.out contain the domain time and the forces and deformations for section 1 (the base section) of element 1. These can be used to generate the moment-curvature time history of the base section of column 1 as shown below.\n\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e \u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e"
      })
      .add(
      
      
      {
        id: 28,
        tag: "en",
        href: "/opensees-gallery/examples/inelasticsdof/",
        title: "Inelastic SDOF",
        description: "Integration of an inelastic single-degree-of-freedom (SDOF) system.",
        
        
        content: "March 2020, By Amir Hossein Namadchi\nThis is an OpenSeesPy simulation of a simple SDOF system with elastoplastic behavior mentioned in Dynamics of Structures book by Ray W. Clough and J. Penzien. This example has been solved in the book, so the result obtained here can be compared with the reference.\nThis notebook is adapted from https://github.com/AmirHosseinNamadchi/OpenSeesPy-Examples/blob/master/Elastoplastic%20SDOF%20system.ipynb\u0026nbsp; import numpy as np import opensees.openseespy as ops import matplotlib.pyplot as plt## Units inch = 1 # inches kips = 1 # KiloPounds sec = 1 # Seconds lb = kips*(sec**2)/inch # mass unit (derived)Model specifications are defined as follows:\nm = 0.1*lb # Mass k = 5.0*(kips/inch) # Stiffness c = 0.2*(kips*sec/inch) # Damping dy_p = 1.2*inch # Plastic state displacment alpha_m = c/m # Rayleigh damping ratio # Variation of p(t) in tabular form load_history = np.array([[0, 0], [0.1, 5], [0.2, 8], [0.3, 7], [0.4, 5], [0.5, 3], [0.6, 2], [0.7, 1], [0.8, 0]]) # Dynamic Analysis Parameters dt = 0.01 time = 1.0 Analysis \u0026nbsp; Let\u0026rsquo;s wrap the whole part in a function so that different material behavior could be passed to the function:\ndef do_analysis(dt, time, material_params): model = ops.Model(ndm=1, ndf=1) time_domain = np.arange(0, time, dt) # Nodes model.node(1,0.0,0.0) model.node(2,0.0,0.0) model.uniaxialMaterial(*material_params) model.element(\u0026#39;ZeroLength\u0026#39;, 1, *[1,2], mat=1, dir=1) model.mass(2, m) model.rayleigh(alpha_m, 0.0, 0.0, 0.0) model.fix(1,1) model.timeSeries(\u0026#39;Path\u0026#39;, 1, values=load_history[:,1], time=load_history[:,0]) model.pattern(\u0026#39;Plain\u0026#39;, 1, 1) model.load(2, 1) # Analysis model.constraints(\u0026#39;Plain\u0026#39;) model.numberer(\u0026#39;Plain\u0026#39;) model.system(\u0026#39;ProfileSPD\u0026#39;) model.test(\u0026#39;NormUnbalance\u0026#39;, 0.0000001, 100) model.algorithm(\u0026#39;ModifiedNewton\u0026#39;) model.integrator(\u0026#39;Newmark\u0026#39;, 0.5, 0.25) model.analysis(\u0026#39;Transient\u0026#39;) time_lst =[0] # list to hold time stations for plotting response = [0] # response params of node 2 for i in range(len(time_domain)): model.analyze(1, dt) time_lst.append(model.getTime()) response.append(model.nodeDisp(2,1)) return \u0026#39;time_list\u0026#39;:np.array(time_lst), \u0026#39;d\u0026#39;: np.array(response)For comparison (similar to the book), elastic analysis is also inculded:\nepp = do_analysis(dt, time, [\u0026#39;ElasticPP\u0026#39;, 1, k, dy_p]) # Elastic-Perfectly Plastic els = do_analysis(dt, time, [\u0026#39;Elastic\u0026#39;, 1, k]) # Elastic Visualization \u0026nbsp; plt.figure(figsize=(7,5)) plt.plot(epp[\u0026#39;time_list\u0026#39;], epp[\u0026#39;d\u0026#39;], color = \u0026#39;#fe4a49\u0026#39;, linewidth=1.75, label = \u0026#39;Nonlinear (EPP)\u0026#39;) plt.plot(els[\u0026#39;time_list\u0026#39;], els[\u0026#39;d\u0026#39;], color = \u0026#39;#2ab7ca\u0026#39;, linewidth=1.75, label = \u0026#39;Linear (Elastic)\u0026#39;) plt.ylabel(\u0026#39;Displacement (inch)\u0026#39;, \u0026#39;fontstyle\u0026#39;:\u0026#39;italic\u0026#39;,\u0026#39;size\u0026#39;:14) plt.xlabel(\u0026#39;Time (sec)\u0026#39;, \u0026#39;fontstyle\u0026#39;:\u0026#39;italic\u0026#39;,\u0026#39;size\u0026#39;:14) plt.xlim([0.0, time]) plt.legend() plt.grid() plt.yticks(fontsize = 14) plt.xticks(fontsize = 14);Output:\n\u0026lt;Figure size 700x500 with 1 Axes\u0026gt; Closure \u0026nbsp; Results obtained here with OpenSees perfectly agree with the ones in the book.\nReferences \u0026nbsp; Clough, R.W. and Penzien, J., 2003. Dynamics of structures. Berkeley. CA: Computers and Structures, Inc. 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 import sdof import numpy as np import opensees.openseespy as op FREE = 0 FIXED = 1 X, Y, RZ = 1, 2, 3 def plastic_sdof(material, motion, dt, xi=0.05, r_post=0.0): \u0026#34;\u0026#34;\u0026#34; Run seismic analysis of a nonlinear SDOF :param mass: mass :param k: spring stiffness :param f_yield: yield strength :param motion: list, acceleration values :param dt: float, time step of acceleration values :param xi: damping ratio :param r_post: post-yield stiffness :return: \u0026#34;\u0026#34;\u0026#34; mass, k, f_yield = material op.wipe() # 2 dimensions, 3 dof per node op.model(\u0026#39;basic\u0026#39;, \u0026#39;-ndm\u0026#39;, 2, \u0026#39;-ndf\u0026#39;, 3) # Establish nodes bot_node = 1 top_node = 2 op.node(bot_node, 0., 0.) op.node(top_node, 0., 0.) # Fix bottom node op.fix(top_node, FREE, FIXED, FIXED) op.fix(bot_node, FIXED, FIXED, FIXED) # Set out-of-plane DOFs to be slaved op.equalDOF(1, 2, *[2, 3]) # nodal mass (weight / g): op.mass(top_node, mass, 0., 0.) # Define material bilinear_mat_tag = 1 mat_type = \u0026#34;Steel01\u0026#34; mat_props = [f_yield, k, r_post] op.uniaxialMaterial(mat_type, bilinear_mat_tag, *mat_props) # Assign zero length element beam_tag = 1 op.element(\u0026#39;zeroLength\u0026#39;, beam_tag, bot_node, top_node, \u0026#34;-mat\u0026#34;, bilinear_mat_tag, \u0026#34;-dir\u0026#34;, 1, \u0026#39;-doRayleigh\u0026#39;, 1) # Define the dynamic analysis load_tag_dynamic = 1 pattern_tag_dynamic = 1 values = list(-1 * motion) # should be negative # op.timeSeries(\u0026#39;Path\u0026#39;, load_tag_dynamic, dt=dt, values=values) op.timeSeries(\u0026#39;Path\u0026#39;, load_tag_dynamic, \u0026#34;-dt\u0026#34;, dt, \u0026#34;-values\u0026#34;, *values) # op.pattern(\u0026#39;UniformExcitation\u0026#39;, pattern_tag_dynamic, X, accel=load_tag_dynamic) op.pattern(\u0026#39;UniformExcitation\u0026#39;, pattern_tag_dynamic, X, \u0026#34;-accel\u0026#34;, load_tag_dynamic) # set damping based on first eigen mode eig = op.eigen(\u0026#39;-fullGenLapack\u0026#39;, 1) try: angular_freq = eig**0.5 except: angular_freq = eig[0]**0.5 alpha_m = 0.0 beta_k = 2 * xi / angular_freq beta_k_comm = 0.0 beta_k_init = 0.0 op.rayleigh(alpha_m, beta_k, beta_k_init, beta_k_comm) # Run the dynamic analysis # op.wipeAnalysis() op.algorithm(\u0026#39;Newton\u0026#39;) # op.system(\u0026#39;SparseGeneral\u0026#39;) op.numberer(\u0026#39;RCM\u0026#39;) op.constraints(\u0026#39;Transformation\u0026#39;) op.integrator(\u0026#39;Newmark\u0026#39;, 0.5, 0.25) op.analysis(\u0026#39;Transient\u0026#39;) tol = 1.0e-10 iterations = 10 op.test(\u0026#39;EnergyIncr\u0026#39;, tol, iterations, 0, 2) analysis_time = (len(values) - 1) * dt analysis_dt = 0.001 outputs =  \u0026#34;time\u0026#34;: [], \u0026#34;rel_disp\u0026#34;: [], \u0026#34;rel_accel\u0026#34;: [], \u0026#34;rel_vel\u0026#34;: [], \u0026#34;force\u0026#34;: []  while op.getTime() \u0026lt; analysis_time: curr_time = op.getTime() if op.analyze(1, analysis_dt) != 0: print(f\u0026#34;Failed at time op.getTime()\u0026#34;) break outputs[\u0026#34;time\u0026#34;].append(curr_time) outputs[\u0026#34;rel_disp\u0026#34;].append(op.nodeDisp(top_node, 1)) outputs[\u0026#34;rel_vel\u0026#34;].append(op.nodeVel(top_node, 1)) outputs[\u0026#34;rel_accel\u0026#34;].append(op.nodeAccel(top_node, 1)) op.reactions() outputs[\u0026#34;force\u0026#34;].append(-op.nodeReaction(bot_node, 1)) # Negative since diff node op.wipe() for item in outputs: outputs[item] = np.array(outputs[item]) return outputs def main(): \u0026#34;\u0026#34;\u0026#34; Create a plot of an elastic analysis, nonlinear analysis and closed form elastic :return: \u0026#34;\u0026#34;\u0026#34; import eqsig import matplotlib.pyplot as plt record_filename = \u0026#39;test_motion_dt0p01.txt\u0026#39; dt = 0.01 rec = np.loadtxt(record_filename) acc_signal = eqsig.AccSignal(rec, dt) period = 1.0 xi = 0.05 mass = 1.0 f_yield = 1.5 # Reduce this to make it nonlinear r_post = 0.0 periods = np.array([period]) k = 4 * np.pi ** 2 * mass / period ** 2 outputs = plastic_sdof((mass, k, f_yield), rec, dt, xi=xi, r_post=r_post) outputs_elastic = plastic_sdof((mass, k, f_yield * 100), rec, dt, xi=xi, r_post=r_post) ux_opensees = outputs[\u0026#34;rel_disp\u0026#34;] ux_opensees_elastic = outputs_elastic[\u0026#34;rel_disp\u0026#34;] print(outputs) bf, sps = plt.subplots(nrows=2) sps[0].plot(outputs[\u0026#34;time\u0026#34;], ux_opensees, label=\u0026#34;OpenSees fy=%.3gN\u0026#34; % f_yield, ls=\u0026#34;-\u0026#34;) sps[0].plot(outputs[\u0026#34;time\u0026#34;], ux_opensees_elastic, label=\u0026#34;OpenSees fy=%.3gN\u0026#34; % (f_yield * 100), ls=\u0026#34;--\u0026#34;) time = acc_signal.time acc_opensees_elastic = np.interp(time, outputs_elastic[\u0026#34;time\u0026#34;], outputs_elastic[\u0026#34;rel_accel\u0026#34;]) - rec resp_u, resp_v, resp_a = sdof.integrate(rec, dt, k, 2*xi*mass*np.sqrt(k/mass), mass, fy=f_yield) sps[0].plot(acc_signal.time, resp_u, label=\u0026#34;sdof\u0026#34;) sps[1].plot(acc_signal.time, resp_a, label=\u0026#34;sdof\u0026#34;) # resp_u, resp_v, resp_a = duhamels.response_series(motion=rec, dt=dt, periods=periods, xi=xi) # sps[0].plot(acc_signal.time, resp_u[0], label=\u0026#34;Eqsig\u0026#34;) # sps[1].plot(acc_signal.time, resp_a[0], label=\u0026#34;Eqsig\u0026#34;) # Elastic solution # print(\u0026#34;diff\u0026#34;, sum(acc_opensees_elastic - resp_a[0])) sps[1].plot(time, acc_opensees_elastic, label=\u0026#34;Opensees fy=%.2gN\u0026#34; % (f_yield * 100), ls=\u0026#34;--\u0026#34;) sps[0].legend() sps[1].legend() plt.show() if __name__ == \u0026#39;__main__\u0026#39;: main()"
      })
      .add(
      
      
      {
        id: 29,
        tag: "en",
        href: "/opensees-gallery/docs/getting-started/introduction/",
        title: "Introduction",
        description: "Get started with OpenSees.",
        
        
        content: "opensees is a Python package that provides an intuitive API for nonlinear finite element analysis, implemented in C++ through the OpenSees framework. OpenSees features state-of-the-art finite element formulations and solution algorithms, including mixed formulations for beams and solids, over 200 material models, and an extensive collection of continuation algorithms to solve highly nonlinear problems.\nInstallation \u0026nbsp; In order to install opensees just run the command:\npython -m pip install opensees Running OpenSees \u0026nbsp; The opensees package can be used in three ways:\nPython Module The opensees.openseespy Python module implements the API that has been developed by Oregon State. Command line interface An interactive Tcl interpreter can be started by invoking the module as follows from the command line:\npython -m opensees --help Interactive Interpreter An interactive Tcl interpreter can be started by invoking the module as follows from the command line:\npython -m opensees"
      })
      .add(
      
      
      {
        id: 30,
        tag: "en",
        href: "/opensees-gallery/docs/configuration/layout/",
        title: "Layout",
        description: "Hinode uses a grid-based, responsive design for the home page, single pages and list pages.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 31,
        tag: "en",
        href: "/opensees-gallery/docs/about/license/",
        title: "License",
        description: "OpenSeesRT's open-source license for the codebase and documentation.",
        
        
        content: "Codebase \u0026nbsp; The codebase of OpenSeesRT is open source under the conditions of the MIT license\u0026nbsp; and is copyright © 2024 by Mark Dumay. In short, the MIT license allows you to use the OpenSeesRT codebase for both personal and commercial use, as long as you include the original license and copyright notice. Licensed works, modifications, and larger works may be distributed under different terms and without source code. No liability or warranty is given.\nDocumentation \u0026nbsp; The documentation of OpenSeesRT is licensed under the Creative Commons ( CC BY-NC 4.0\u0026nbsp; ) license. This includes all files within the repository\u0026rsquo;s /content and /exampleSite/content folders and their children, as well as the \u0026ldquo;README\u0026rdquo; in the repository root. The license allows you to share and adapt the materials, as long as you give appropriate credit and do not use the materials for commercial purposes. No warranties are given. p"
      })
      .add(
      
      
      {
        id: 32,
        tag: "en",
        href: "/opensees-gallery/examples/chopra-10.4/",
        title: "Matrix Eigenvalue Analysis",
        description: "This example demonstrates how to perform eigenvalue analysis and plot mode shapes. ",
        
        
        content: "This example is adapted from the OpenSees Wiki page Eigen analysis of a two-storey shear frame\u0026nbsp; .\nThis example demonstrates how to perform eigenvalue analysis and plot mode shapes.\nAn idealized two-storey shear frame (Example 10.4 from \u0026ldquo;Dynamic of Structures\u0026rdquo; book by Professor Anil K. Chopra) is used for this purpose. In this idealization beams are rigid in flexure, axial deformation of beams and columns are neglected, and the effect of axial force on the stiffness of the columns is neglected. Geometry and material characteristics of the frame structure are shown in Figure 1. Node and element numbering is given in Figure 2.\nShearFrame5.png Instructions on how to run this example \u0026nbsp; To execute this ananlysis in OpenSees the user has to download this files:\nEigenAnal_twoStoryShearFrame.tcl Place EigenAnal_twoStoryShearFrame.tcl in the same folder with the OpenSees.exe. By double clicking on OpenSees.exe the OpenSees interpreter will pop out. To run the analysis the user should type:\nPython Tcl python EigenAnal_twoStoryShearFrame8.py python -m opensees EigenAnal_twoStoryShearFrame8.tcl and hit enter. To create output files (stored in directory \u0026ldquo;data\u0026rdquo;) the user has to exit OpenSees interpreter by typing \u0026ldquo;exit\u0026rdquo;.\nCreate the model \u0026nbsp; Spatial dimension of the model and number of degrees-of-freedom (DOF) at nodes are defined using model command. In this example we have 2D model with 3 DOFs at each node. This is defined in the following way:\nPython Tcl import opensees.openseespy as ops model = ops.Model(ndm=2, ndf=3) model BasicBuilder -ndm 2 -ndf 3 Note: geometry, mass, and material characteristics are assigned to variables that correspond to the ones shown in Figure 1 (e.g., the height of the column is set to be 144 in. and assigned to variable h; the value of the height can be accessed by $h).\nNodes of the structure (Figure 2) are defined using the node command:\nPython Tcl model.node(1, 0., 0.) model.node(2, L , 0.) model.node(3, 0., h ) model.node(4, L , h ) model.node(5, 0., 2*h ) model.node(6, L , 2*h ) node 1 0. 0. ; node 2 $L 0. ; node 3 0. $h ; node 4 $L $h ; node 5 0. [expr 2*$h]; node 6 $L [expr 2*$h]; The boundary conditions are defined next using single-point constraint command fix. In this example nodes 1 and 2 are fully fixed at all three DOFs:\nPython Tcl model.fix(1, 1, 1, 1) model.fix(2, 1, 1, 1) fix 1 1 1 1; fix 2 1 1 1; Masses are assigned at nodes 3, 4, 5, and 6 using mass command. Since the considered shear frame system has only two degrees of freedom (displacements in x at the 1st and the 2nd storey), the masses have to be assigned in x direction only.\nPython Tcl model.mass(3, m , 0., 0. ) model.mass(4, m , 0., 0. ) model.mass(5, m/2., 0., 0. ) model.mass(6, m/2., 0., 0. ) mass 3 $m 0. 0. ; mass 4 $m 0. 0. ; mass 5 [expr $m/2.] 0. 0. ; mass 6 [expr $m/2.] 0. 0. ; The geometric transformation with id tag 1 is defined to be linear.\nset TransfTag 1; geomTransf Linear $TransfTag ; The beams and columns of the frame are defined to be elastic using elasticBeamColumn element. In order to make beams infinitely rigid moment of inertia for beams (Ib) is set to very high value (10e+12).\nPython Tcl model.element(\u0026#34;ElasticBeamColumn\u0026#34;, 1, 1, 3, Ac, Ec, 2.*Ic, TransfTag) model.element(\u0026#34;ElasticBeamColumn\u0026#34;, 2, 3, 5, Ac, Ec, Ic, TransfTag) model.element(\u0026#34;ElasticBeamColumn\u0026#34;, 3, 2, 4, Ac, Ec, 2.*Ic, TransfTag) model.element(\u0026#34;ElasticBeamColumn\u0026#34;, 4, 4, 6, Ac, Ec, Ic, TransfTag) model.element(\u0026#34;ElasticBeamColumn\u0026#34;, 5, 3, 4, Ab, E, Ib, TransfTag) model.element(\u0026#34;ElasticBeamColumn\u0026#34;, 6, 5, 6, Ab, E, Ib, TransfTag) element elasticBeamColumn 1 1 3 $Ac $Ec [expr 2.*$Ic] $TransfTag; element elasticBeamColumn 2 3 5 $Ac $Ec $Ic $TransfTag; element elasticBeamColumn 3 2 4 $Ac $Ec [expr 2.*$Ic] $TransfTag; element elasticBeamColumn 4 4 6 $Ac $Ec $Ic $TransfTag; element elasticBeamColumn 5 3 4 $Ab $E $Ib $TransfTag; element elasticBeamColumn 6 5 6 $Ab $E $Ib $TransfTag; To comply with the assumptions of the shear frame (no vertical displacemnts and rotations at nodes) end nodes of the beams are constrained to each other in the 2nd DOF (vertical displacement) and the 3rd DOF (rotation). EqualDOF command is used to imply these constraints.\nequalDOF 3 4 2 3; equalDOF 5 6 2 3; Define recorders \u0026nbsp; For the specified number of eigenvalues (numModes) (for this example it is 2) the eigenvectors are recorded at all nodes in all DOFs using node recorder command.\nPython Tcl for k in range(numModes): model.recorder(\u0026#34;Node\u0026#34;, f\u0026#34;eigen k\u0026#34;, file=f\u0026#34;modes/modek.out\u0026#34;, nodeRange=[1, 6], dof=[1, 2, 3]) foreach k [range $numModes]  recorder Node -file [format \u0026#34;modes/mode%i.out\u0026#34; $k] -nodeRange 1 6 -dof 1 2 3 \u0026#34;eigen $k\u0026#34;  Perform eigenvalue analysis and store periods into a file \u0026nbsp; The eigenvalues are calculated using eigen commnad and stored in lambda variable.\nset lambda [eigen $numModes];The periods and frequencies of the structure are calculated next.\nset omega  set f  set T  set pi 3.141593 foreach lam $lambda  lappend omega [expr sqrt($lam)]; lappend f [expr sqrt($lam)/(2*$pi)]; lappend T [expr (2*$pi)/sqrt($lam)]; The periods are stored in a Periods.txt file inside of directory modes/.\nset period \u0026#34;modes/Periods.txt\u0026#34; set Periods [open $period \u0026#34;w\u0026#34;] foreach t $T  puts $Periods \u0026#34; $t\u0026#34;  close $Periods Record the eigenvectors \u0026nbsp; For eigenvectors to be recorded record command has to be issued following the eigen command.\nrecord Display mode shapes \u0026nbsp; TODO\nExample Provided by: Vesna Terzic, UC Berkeley"
      })
      .add(
      
      
      {
        id: 33,
        tag: "en",
        href: "/opensees-gallery/docs/getting-started/modeling/",
        title: "Modeling",
        description: "Modeling in Python \u0026nbsp; The best practice for modeling in Python is to create a model class by calling the opensees.openseespy.Model(...) constructor (note the capital \u0026ldquo;M\u0026rdquo;). All standard OpenSees functions, as documented here\u0026nbsp; can be called as methods on the object that is retured. For example:\n",
        
        
        content: "Modeling in Python \u0026nbsp; The best practice for modeling in Python is to create a model class by calling the opensees.openseespy.Model(...) constructor (note the capital \u0026ldquo;M\u0026rdquo;). All standard OpenSees functions, as documented here\u0026nbsp; can be called as methods on the object that is retured. For example:\nimport opensees.openseespy as ops model = ops.Model(ndm=2, ndf=3) model.node(1, 2.0, 3.0) Evaluate Tcl models from Python \u0026nbsp; The first scripting interface to OpenSees used a programming language called Tcl, which continues to be supported. To execute Tcl commands from a Python script, just create an instance of the opensees.openseespy.Model class and call its eval() method:\nimport opensees.openseespy as ops model = ops.Model() model.eval(\u0026#34;model Basic -ndm 2\u0026#34;) model.eval(\u0026#34;print -json\u0026#34;)Full Tcl files can be conveniently executed in this way. For example, if a Tcl file called model.tcl exists in the current working directory:\nimport opensees.openseespy as ops model = ops.Model() with open(\u0026#34;model.tcl\u0026#34;, \u0026#34;r\u0026#34;) as f: model.eval(f.read())"
      })
      .add(
      
      
      {
        id: 34,
        tag: "en",
        href: "/opensees-gallery/docs/advanced-settings/module-development/",
        title: "Module development",
        description: "Develop your own Hugo modules compatible with Hinode.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 35,
        tag: "en",
        href: "/opensees-gallery/examples/example2/",
        title: "Moment-Curvature Analysis",
        description: "A reinforced concrete cross-section is modeled using a fiber section,  and a moment-curvature analysis is performed.",
        
        
        content: "This example performs a moment-curvature analysis of a reinforced concrete section which is represented by a fiber discretization. Because we are only interested in the response quantities of the cross section, a zero-length element is used to wrap the cross section.\nModeling \u0026nbsp; The figure below shows the fiber discretization for the section. The files for this example are: Python Tcl \u0026lt;a href=\u0026quot;Example2.py\u0026quot;\u0026gt;\u0026lt;code\u0026gt;Example2.py\u0026lt;/code\u0026gt;\u0026lt;/a\u0026gt;\u0026lt;/li\u0026gt; \u0026lt;a href=\u0026quot;Example2.tcl\u0026quot;\u0026gt;\u0026lt;code\u0026gt;Example2.tcl\u0026lt;/code\u0026gt;\u0026lt;/a\u0026gt;\u0026lt;/li\u0026gt; \u0026lt;a href=\u0026quot;MomentCurvature.tcl\u0026quot;\u0026gt;\u0026lt;code\u0026gt;MomentCurvature.tcl\u0026lt;/code\u0026gt;\u0026lt;/a\u0026gt;\u0026lt;/li\u0026gt; The model consists of two nodes and a ZeroLengthSection element. A depiction of the element geometry is shown in figure zerolength. The drawing on the left of figure zerolength shows an edge view of the element where the local zz -axis, as seen on the right side of the figure and in figure rcsection0, is coming out of the page. Node 1 is completely restrained, while the applied loads act on node 2. A compressive axial load, PP , of 180180 kips is applied to the section during the moment-curvature analysis.\nA fiber section is created by grouping various patches and layers:\nNote in Python you must pass the section tag when calling patch and layer\nPython Tcl model.section(\u0026#34;Fiber\u0026#34;, 1) # Create the concrete core fibers model.patch(\u0026#34;rect\u0026#34;, 1, 10, 1, cover-y1, cover-z1, y1-cover, z1-cover, section=1) # Create the concrete cover fibers (top, bottom, left, right, section=1) model.patch(\u0026#34;rect\u0026#34;, 2, 10, 1, -y1, z1-cover, y1, z1, section=1) model.patch(\u0026#34;rect\u0026#34;, 2, 10, 1, -y1, -z1, y1, cover-z1, section=1) model.patch(\u0026#34;rect\u0026#34;, 2, 2, 1, -y1, cover-z1, cover-y1, z1-cover, section=1) model.patch(\u0026#34;rect\u0026#34;, 2, 2, 1, y1-cover, cover-z1, y1, z1-cover, section=1) # Create the reinforcing fibers (left, middle, right, section=1) model.layer(\u0026#34;straight\u0026#34;, 3, 3, As, y1-cover, z1-cover, y1-cover, cover-z1, section=1) model.layer(\u0026#34;straight\u0026#34;, 3, 2, As, 0.0, z1-cover, 0.0, cover-z1, section=1) model.layer(\u0026#34;straight\u0026#34;, 3, 3, As, cover-y1, z1-cover, cover-y1, cover-z1, section=1) section Fiber 1  # Create the concrete core fibers patch rect 1 10 1 [expr $cover-$y1] [expr $cover-$z1] [expr $y1-$cover] [expr $z1-$cover] # Create the concrete cover fibers (top, bottom, left, right) patch rect 2 10 1 [expr -$y1] [expr $z1-$cover] $y1 $z1 patch rect 2 10 1 [expr -$y1] [expr -$z1] $y1 [expr $cover-$z1] patch rect 2 2 1 [expr -$y1] [expr $cover-$z1] [expr $cover-$y1] [expr $z1-$cover] patch rect 2 2 1 [expr $y1-$cover] [expr $cover-$z1] $y1 [expr $z1-$cover] # Create the reinforcing fibers (left, middle, right) layer straight 3 3 $As [expr $y1-$cover] [expr $z1-$cover] [expr $y1-$cover] [expr $cover-$z1] layer straight 3 2 $As 0.0 [expr $z1-$cover] 0.0 [expr $cover-$z1] layer straight 3 3 $As [expr $cover-$y1] [expr $z1-$cover] [expr $cover-$y1] [expr $cover-$z1]  For the zero length element, a section discretized by concrete and steel is created to represent the resultant behavior. UniaxialMaterial objects are created to define the fiber stress-strain relationships: confined concrete in the column core, unconfined concrete in the column cover, and reinforcing steel.\nThe dimensions of the fiber section are shown in figure rcsection0. The section depth is 24 inches, the width is 15 inches, and there are 1.5 inches of cover around the entire section. Strong axis bending is about the section zz -axis. In fact, the section zz -axis is the strong axis of bending for all fiber sections in planar problems. The section is separated into confined and unconfined concrete regions, for which separate fiber discretizations will be generated. Reinforcing steel bars will be placed around the boundary of the confined and unconfined regions. The fiber discretization for the section is shown in figure rcsection4.\nAnalysis \u0026nbsp; The section analysis is performed by the procedure moment_curvature defined in the file MomentCurvature.tcl for Tcl, and Example2.1.py for Python. The arguments to the procedure are the tag secTag of the section to be analyzed, the axial load axialLoad applied to the section, the maximum curvature maxK, and the number numIncr of displacement increments to reach the maximum curvature.\nThe output for the moment-curvature analysis will be the section forces and deformations, stored in the file section1.out. In addition, an estimate of the section yield curvature is printed to the screen.\nIn the moment_curvature procedure, the nodes are defined to be at the same geometric location and the ZeroLengthSection element is used. A single load step is performed for the axial load, then the integrator is changed to DisplacementControl to impose nodal displacements, which map directly to section deformations. A reference moment of 1.0 is defined in a Linear time series. For this reference moment, the DisplacementControl integrator will determine the load factor needed to apply the imposed displacement. A node recorder is defined to track the moment-curvature results. The load factor is the moment, and the nodal rotation is in fact the curvature of the element with zero thickness.\nThe expected output is:\nEstimated yield curvature: 0.000126984126984 The file section1.out contains for each committed state a line with the load factor and the rotation at node 3. This can be used to plot the moment-curvature relationship as shown in figure momcurv."
      })
      .add(
      
      
      {
        id: 36,
        tag: "en",
        href: "/opensees-gallery/examples/framebuckling/",
        title: "Nonlinear Geometry",
        description: "Corotational frame elements are used to approximate Euler\u0026rsquo;s buckling load, which is given by: Peuler=π2EIL2 P_{\\mathrm{euler}} = \\frac{\\pi^2 EI}{L^2} This example is adapted from https://github.com/denavit/OpenSees-Examples\u0026nbsp; . The files for the problem are buckling.py for Python, and buckling.tcl for Tcl.\n",
        
        
        content: "Corotational frame elements are used to approximate Euler\u0026rsquo;s buckling load, which is given by: Peuler=π2EIL2 P_\\mathrmeuler = \\frac\\pi^2 EIL^2 This example is adapted from https://github.com/denavit/OpenSees-Examples\u0026nbsp; . The files for the problem are buckling.py for Python, and buckling.tcl for Tcl.\nTheory \u0026nbsp; Buckling Analysis \u0026nbsp; Loosely speaking, buckling happens when there are multiple shapes that a structure can deform into that will be in equilibrium with it\u0026rsquo;s applied loads. This implies that at the point of buckling, there are multiple independent displacement increments u\\bmu which will be mapped to the same resisting load by the tangent K\\bmK . In otherwords, The buckling load is the point at which K\\bmK becomes singular. If we consider K\\bmK as a function of the load factor λ\\bm\\lambda , this condition can be expressed as the nonlinear root-finding problem: det⁡K(λ)=0 \\operatornamedet\\bmK(\\lambda) = 0 For many classical models, the dependence of K\\bmK on λ\\lambda is linear, and in this case the problem is equivalent to a generalized eigenvalue problem which is computationally much more tractable. However, even if K\\bmK is nonlinear in λ\\lambda , one may still investigate the linearized buckling problem, where an eigenvalue problem is obtained by learizing K(λ)\\bmK(\\lambda) : K(λ)≈K(0)+K′(0)λ \\bmK(\\lambda) \\approx \\bmK(0) + \\bmK^\\prime(0) \\lambda where K′\\bmK^\\prime is the derivative of K\\bmK with respect to λ\\lambda .\nTimoshenko Column Buckling \u0026nbsp; λ=PL2EI[1−P/(ksGA)]=PL2χEIχ=1−P/(ksGA)P=χλ2EI/L2. \\begingathered \\lambda=\\sqrt\\fracP L^2E I\\left[1-P /\\left(k_\\mathrms G A\\right)\\right]=\\sqrt\\fracP L^2\\chi E I \\\\ \\chi=1-P /\\left(k_\\mathrms G A\\right) \\\\ P=\\chi \\lambda^2 E I / L^2 . \\endgathered χ=11+λ2EI/(ksGAL2)=11+λ2φ/12P=λ2EI/L21+λ2φ/12. \\begingathered \\chi=\\frac11+\\lambda^2 E I /\\left(k_\\mathrms G A L^2\\right)=\\frac11+\\lambda^2 \\varphi / 12 \\\\ P=\\frac\\lambda^2 E I / L^21+\\lambda^2 \\varphi / 12 . \\endgathered tan⁡λcr =χλcr =λcr 1+λcr 2φ/12 \\tan \\lambda_\\text cr =\\chi \\lambda_\\text cr =\\frac\\lambda_\\text cr 1+\\lambda_\\text cr  2 \\varphi / 12"
      })
      .add(
      
      
      {
        id: 37,
        tag: "en",
        href: "/opensees-gallery/docs/advanced-settings/overview/",
        title: "Overview",
        description: "Configure and customize Hinode to your liking using modules, npm, and mounted folders.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 38,
        tag: "en",
        href: "/opensees-gallery/docs/advanced-settings/partial-development/",
        title: "Partial development",
        description: "Develop custom partials and shortcodes following Hinode's coding conventions.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 39,
        tag: "en",
        href: "/opensees-gallery/docs/getting-started/python/",
        title: "Python",
        description: "",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 40,
        tag: "en",
        href: "/opensees-gallery/releases/",
        title: "Releases",
        description: "A chronological overview of key releases since the initial launch of Hinode.",
        
        
        content: "The timeline below captures the significant changes since the initial release of Hinode in April, 2022. Visit GitHub for a full overview of all Hinode releases\u0026nbsp; , including features, bug fixes, and dependency upgrades.\nRender hooks v0.26.0 August 15, 2024\nThis release includes support for markdown links and markdown images. Hinode will invoke the relevant partials, so they will have the same behavior and styling as their counterparts. This release also includes support for server-side math rendering as introduced by Hugo v0.132.0\u0026nbsp; .\nScript bundle localization v0.25.0 August 2, 2024\nHinode includes search support out of the box. To limit the bundle size, the search index now includes entries for the current translation only. To enable localization, the module configuration includes a new parameter localize. By default, the FlexSearch module sets localization to true.\nInitial launch v0.1 April 13, 2022\nInspired by Blist and Doks, this release introduces Hinode - a modern blog and documentation theme for Hugo. By taking advantage of npm, the used dependencies are easily tracked and updated. Powered by Bootstrap, the generated website is responsive and brings many common UI elements. Hinode wraps many of these elements in a shortcode to simplify their usage.\nRender hooks v0.26.0 August 15, 2024\nThis release includes support for markdown links and markdown images. Hinode will invoke the relevant partials, so they will have the same behavior and styling as their counterparts. This release also includes support for server-side math rendering as introduced by Hugo v0.132.0\u0026nbsp; .\nScript bundle localization v0.25.0 August 2, 2024\nHinode includes search support out of the box. To limit the bundle size, the search index now includes entries for the current translation only. To enable localization, the module configuration includes a new parameter localize. By default, the FlexSearch module sets localization to true.\nInitial launch v0.1 April 13, 2022\nInspired by Blist and Doks, this release introduces Hinode - a modern blog and documentation theme for Hugo. By taking advantage of npm, the used dependencies are easily tracked and updated. Powered by Bootstrap, the generated website is responsive and brings many common UI elements. Hinode wraps many of these elements in a shortcode to simplify their usage."
      })
      .add(
      
      
      {
        id: 41,
        tag: "en",
        href: "/opensees-gallery/examples/spectrum/",
        title: "RotD Spectrum",
        description: "This code computes the RotD50 Sa and RotD100 Sa Spectra of bi-directional ground motion records.\nspectra.py\n",
        
        
        content: "This code computes the RotD50 Sa and RotD100 Sa Spectra of bi-directional ground motion records.\nspectra.py\nThe source code for this problem is adapted from the example by Jawad Fayaz at https://openseespydoc.readthedocs.io/en/latest/src/exampleRotDSpectra.html\u0026nbsp; ."
      })
      .add(
      
      
      {
        id: 42,
        tag: "en",
        href: "/opensees-gallery/examples/sathertower/",
        title: "Sather Tower",
        description: "",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 43,
        tag: "en",
        href: "/opensees-gallery/docs/advanced-settings/scripts/",
        title: "Scripts",
        description: "Automatically bundle local and external JavaScript files into a single file.",
        
        
        content: "Hinode bundles local JavaScript files and JavaScript files defined in a core module into a single file. By utilizing Hugo modules, external JavaScript files are automatically ingested and kept up to date."
      })
      .add(
      
      
      {
        id: 44,
        tag: "en",
        href: "/opensees-gallery/examples/sensitivity/",
        title: "Sensitivity",
        description: "Basic sensitivity analysis is performed",
        
        
        content: "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 import opensees.openseespy as ops # Input [N, m, kg, sec] L = 5.0 # Total length of cantilever F = 300000.0 # Lateral point load P = 0.0 # Axial force w = 10000.0 # Distributed load E = 200e9 # Modulus of elasticity G = E*0.6 hw = 0.355 # Web height bf = 0.365 # Flange width tf = 0.018 # Flange thickness tw = 0.011 # Web thickness nf = 3 # Number of fibers in the flange nw = 8 # Number of fibres in the web nel = 1 # Area and moment of inertia A = tw * (hw - 2 * tf) + 2 * bf * tf I = tw * (hw - 2 * tf) ** 3 / 12.0 + 2 * bf * tf * (0.5 * (hw - tf)) ** 2 Ay = A*1e5 Az = A*1e5 Iz = I Iy = I J = 2*I model = ops.Model(ndm=3, ndf=6) model.node(1, 0, 0, 0) model.node(2, L, 0, 0) model.fix(1, 1, 1, 1, 1, 1, 1) model.section(\u0026#34;FrameElastic\u0026#34;, 1, E=E, A=A, Ay=Ay, Az=Az, Iz=Iz, Iy=Iy, J=J, G=G) model.geomTransf(\u0026#34;Linear\u0026#34;, 1, (0, 0, 1)) model.element(\u0026#34;CubicFrame\u0026#34;, 1, (1, 2), section=1, transform=1) model.parameter(1, \u0026#34;element\u0026#34;, 1, \u0026#34;E\u0026#34;) model.parameter(2, \u0026#34;element\u0026#34;, 1, \u0026#34;A\u0026#34;) model.parameter(3, \u0026#34;element\u0026#34;, 1, \u0026#34;Iz\u0026#34;) model.parameter(4, \u0026#34;node\u0026#34;, nel+1, \u0026#34;coord\u0026#34;, 1) model.pattern(\u0026#34;Plain\u0026#34;, 1, \u0026#34;Linear\u0026#34;) model.load(2, (0.0, 1.0, 0.0, 0.0, 0.0, 0.0), pattern=1) model.constraints(\u0026#34;Plain\u0026#34;) model.system(\u0026#34;ProfileSPD\u0026#34;) if True: Pmax = F Nsteps = 1 dP = Pmax / Nsteps model.integrator(\u0026#34;LoadControl\u0026#34;, dP) model.analysis(\u0026#34;Static\u0026#34;) model.sensitivityAlgorithm(\u0026#34;-computeAtEachStep\u0026#34;) for i in range(Nsteps): print(model.analyze(1)) print(model.nodeDisp(2, 2), model.getLoadFactor(1)) for param in model.getParamTags(): print(\u0026#34;\\t\u0026#34;, param, model.sensNodeDisp(2, 2, param)) if False: model.wipeAnalysis() Umax = 2.2 Nsteps = 100 Uincr = Umax/Nsteps model.integrator(\u0026#34;DisplacementControl\u0026#34;,2,2,Uincr) model.analysis(\u0026#34;Static\u0026#34;) model.sensitivityAlgorithm(\u0026#34;-computeAtEachStep\u0026#34;) for i in range(Nsteps): model.analyze(1) print(model.nodeDisp(2,1), model.getLoadFactor(1)) for param in model.getParamTags(): print(param, model.sensLambda(1, param)) # print(param, model.sensNodeDisp(2, 1, param)) print(\u0026#34;u\u0026#34;, F*L**3/(3*E*I)) print(\u0026#34;L\u0026#34;, F*L**2/(E*I)) print(\u0026#34;F\u0026#34;, L**3/(3*E*I))"
      })
      .add(
      
      
      {
        id: 45,
        tag: "en",
        href: "/opensees-gallery/examples/shallowdome/",
        title: "Shallow Dome",
        description: "Double-Layer Shallow Dome \u0026nbsp; March 2020, Amir Hossein Namadchi \u0026nbsp; This is an OpenSeesPy simulation of one of the numerical examples in our previously published paper\u0026nbsp; . The Core was purely written in Mathematica. This is my attempt to perform the analysis again via Opensees Core, to see if I can get the similar results. In the paper, we used Total Lagrangian framework to model the structure. Unfortunately, OpenSees does not include this framework, so, alternatively, I will use Corotational truss element.\n",
        
        
        content: "Double-Layer Shallow Dome \u0026nbsp; March 2020, Amir Hossein Namadchi \u0026nbsp; This is an OpenSeesPy simulation of one of the numerical examples in our previously published paper\u0026nbsp; . The Core was purely written in Mathematica. This is my attempt to perform the analysis again via Opensees Core, to see if I can get the similar results. In the paper, we used Total Lagrangian framework to model the structure. Unfortunately, OpenSees does not include this framework, so, alternatively, I will use Corotational truss element.\nimport numpy as np import opensees.openseespy as ops import matplotlib.pyplot as plt import sees # %matplotlib notebook # %matplotlib widgetBelow, the base units are defined as python variables:\n## Units m = 1 # Meters KN = 1 # KiloNewtons s = 1 # Seconds Model Defintion \u0026nbsp; The coordinates information for each node are stored node_coords. Each row represent a node with the corresponding coordinates. Elements configuration are also described in connectivity, each row representing an element with its node IDs. Elements cross-sectional areas are stored in area_list. This appraoch, offers a more pythonic and flexible code when building the model. Since this is a relatively large model, some data will be read from external .txt files to keep the code cleaner.\n# Node Coordinates Matrix (size : nn x 3) node_coords = np.loadtxt(\u0026#39;assets/nodes.txt\u0026#39;, dtype = np.float64) * m # Element Connectivity Matrix (size: nel x 2) connectivity = np.loadtxt(\u0026#39;assets/connectivity.txt\u0026#39;, dtype = np.int64).tolist() # Loaded Nodes loaded_nodes = np.loadtxt(\u0026#39;assets/loaded_nodes.txt\u0026#39;, dtype = np.int64).tolist() # Get Number of total Nodes nn = len(node_coords) # Get Number of total Elements nel = len(connectivity) # Cross-sectional area list (size: nel) area_list = np.ones(nel)*(0.001)*(m**2) # Modulus of Elasticity list (size: nel) E_list = np.ones(nel)*(2.0*10**8)*(KN/m**2) # Mass Density rho = 7.850*((KN*s**2)/(m**4)) #Boundary Conditions (size: fixed_nodes x 4) B_C = np.column_stack((np.arange(1,31), np.ones((30,3), dtype = np.int64)) ).tolist() Model Construction \u0026nbsp; I use list comprehension to add nodes,elements and other objects to the domain.\nmodel = ops.Model(ndm=3, ndf=3) # Adding nodes to the model object using list comprehensions [model.node(n+1,*node_coords[n]) for n in range(nn)]; # Applying BC [model.fix(B_C[n][0],*B_C[n][1:]) for n in range(len(B_C))]; # Set Material model.uniaxialMaterial(\u0026#39;Elastic\u0026#39;,1, E_list[0]) # Adding Elements [model.element(\u0026#39;corotTruss\u0026#39;, e+1, *connectivity[e], area_list[e], 1,\u0026#39;-rho\u0026#39;, rho*area_list[e], \u0026#39;-cMass\u0026#39;, 1) for e in range(nel)]; Draw model \u0026nbsp; The model can now be drawn using the sees Python package:\nsees.render(model)Output:\n\u0026lt;Figure size 640x480 with 1 Axes\u0026gt;\u0026lt;sees.SkeletalRenderer at 0x7fb589684a90\u0026gt; Eigenvalue Analysis \u0026nbsp; Let\u0026rsquo;s get the first 6 periods of the structure to see if they coincide with the ones in paper.\neigenvalues = model.eigen(6) T_list = 2*np.pi/np.sqrt(eigenvalues) print(\u0026#39;The first 6 period of the structure are as follows:\\n\u0026#39;, T_list)Output:\nThe first 6 period of the structure are as follows: [0.07189215 0.06809579 0.06809578 0.04648394 0.04648388 0.03117022] Dynamic Analysis \u0026nbsp; Great accordance is obtained in eigenvalue analysis. Now, let\u0026rsquo;s do wipeAnalysis() and perform dynamic analysis. The Newmark time integration algorithm with γ=0.5\\gamma=0.5 and β=0.25\\beta=0.25 (Constant Average Acceleration Algorithm) is used. Harmonic loads are applied vertically on the loaded_nodes nodes.\nmodel.wipeAnalysis() # define load function P = lambda t: 250*np.sin(250*t) # Dynamic Analysis Parameters dt = 0.00025 time = 0.2 time_domain = np.arange(0,time,dt) # Adding loads to the domain beautifully model.timeSeries(\u0026#39;Path\u0026#39;, 1, dt=dt, values=np.vectorize(P)(time_domain), time=time_domain) model.pattern(\u0026#39;Plain\u0026#39;, 1, 1) for n in loaded_nodes: model.load(n, *[0,0,-1]) # Analysis model.constraints(\u0026#39;Plain\u0026#39;) model.numberer(\u0026#39;Plain\u0026#39;) model.system(\u0026#39;ProfileSPD\u0026#39;) model.test(\u0026#39;NormUnbalance\u0026#39;, 0.0000001, 100) model.algorithm(\u0026#39;ModifiedNewton\u0026#39;) model.integrator(\u0026#39;Newmark\u0026#39;, 0.5, 0.25) model.analysis(\u0026#39;Transient\u0026#39;)time_lst =[] # list to hold time stations for plotting d_apex_list = [] # list to hold vertical displacments of the apex for i in range(len(time_domain)): is_done = model.analyze(1, dt) if is_done != 0: print(\u0026#39;Failed to Converge!\u0026#39;) break time_lst.append(model.getTime()) d_apex_list.append(model.nodeDisp(362,3)) Visualization \u0026nbsp; Below, the time history of the vertical displacement of the apex is plotted.\nplt.figure(figsize=(12,4)) plt.plot(time_lst, np.array(d_apex_list), color = \u0026#39;#d62d20\u0026#39;, linewidth=1.75) plt.ylabel(\u0026#39;Vertical Displacement (m)\u0026#39;, \u0026#39;fontstyle\u0026#39;:\u0026#39;italic\u0026#39;,\u0026#39;size\u0026#39;:14) plt.xlabel(\u0026#39;Time (sec)\u0026#39;, \u0026#39;fontstyle\u0026#39;:\u0026#39;italic\u0026#39;,\u0026#39;size\u0026#39;:14) plt.xlim([0.0, time]) plt.grid() plt.yticks(fontsize = 14) plt.xticks(fontsize = 14);Output:\n\u0026lt;Figure size 1200x400 with 1 Axes\u0026gt; Closure \u0026nbsp; Very good agreements with the paper are obtained.\nNamadchi, Amir Hossein, Farhang Fattahi, and Javad Alamatian. \"Semiexplicit Unconditionally Stable Time Integration for Dynamic Analysis Based on Composite Scheme.\" Journal of Engineering Mechanics 143, no. 10 (2017): 04017119."
      })
      .add(
      
      
      {
        id: 46,
        tag: "en",
        href: "/opensees-gallery/examples/shellframe/",
        title: "Shell Diaphragms",
        description: "",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 47,
        tag: "en",
        href: "/opensees-gallery/examples/pendulum/",
        title: "Simple Pendulum",
        description: "This example investigates a simple pendulum using the corotational truss element.",
        
        
        content: "This example investigates a simple pendulum using the corotational truss element.\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 # # Adapted from https://portwooddigital.com/2022/08/14/parametric-oscillator/ # # Claudio Perez # import opensees.openseespy as ops def create_pendulum(m, k, L, W): # Create a model with 2 dimensions (ndm) # and 2 degrees of freedom per node (ndf) model = ops.Model(ndm=2, ndf=2) # Create a node for the pivot point and fix it model.node(1, 0, L); model.fix(1, 1, 1) # Create a free node with the mass model.node(2, 0, 0); model.mass(2, m, m) # Create a corotational truss between nodes 1 and 2 model.uniaxialMaterial(\u0026#39;Elastic\u0026#39;, 1, k*L) model.element(\u0026#39;CorotTruss\u0026#39;, 1, 1, 2, 1.0, 1) # Initial displacements model.setNodeDisp(2, 1, 0.05*L, \u0026#39;-commit\u0026#39;) model.setNodeDisp(2, 2, -W/k-(W/k+L)/3, \u0026#39;-commit\u0026#39;) # Pendulum weight model.timeSeries(\u0026#39;Constant\u0026#39;, 1) model.pattern(\u0026#39;Plain\u0026#39;, 1, 1) model.load(2, 0, -W) return model def analyze_pendulum(model): model.algorithm(\u0026#39;Newton\u0026#39;) model.integrator(\u0026#39;Newmark\u0026#39;,0.5,0.25) model.analysis(\u0026#39;Transient\u0026#39;) Tmax = 12*sec dt = 0.01*sec Nsteps = int(Tmax/dt) u = [] for i in range(Nsteps): model.analyze(1, dt) u.append(model.nodeDisp(2)) return u if __name__ == \u0026#34;__main__\u0026#34;: from opensees.units.ips import inch, sec, gravity as g # Length of pendulum L = 10*inch # Pendulum mass m = 1.0 # Frequency of pendulum omega = (g/L)**0.5 # Frequency of oscillator w = 2*omega # Stiffness of spring k = m*w**2 model = create_pendulum(m, k, L, m*g) u = analyze_pendulum(model) print(u)"
      })
      .add(
      
      
      {
        id: 48,
        tag: "en",
        href: "/opensees-gallery/examples/example6/",
        title: "Simply Supported Solid Beam",
        description: "In this example a simply supported beam is modelled with two dimensional solid elements. The example is implemented in both Tcl and Python:\nExample6.tcl Example6.py Each node of the analysis has two displacement degrees of freedom. Thus the model is defined with ndm = 2 and ndf = 2.\n",
        
        
        content: "In this example a simply supported beam is modelled with two dimensional solid elements. The example is implemented in both Tcl and Python:\nExample6.tcl Example6.py Each node of the analysis has two displacement degrees of freedom. Thus the model is defined with ndm = 2 and ndf = 2.\nA mesh is generated using the block2D command. The number of nodes in the local xx -direction of the block is nxnx and the number of nodes in the local yy -direction of the block is nyny . The block2D generation nodes 1,2,3,4 are prescribed to define the two dimensional domain of the beam, which is of size 40×1040\\times10 .\nThree different quadrilateral elements can be used for the analysis. These may be created using the names \u0026quot;BbarQuad\u0026quot;, \u0026quot;EnhancedQuad\u0026quot; or \u0026quot;Quad\u0026quot;. This is a plane strain problem. An elastic isotropic material is used.\nFor initial gravity load analysis, a single load pattern with a linear time series and two vertical nodal loads are used.\nA solution algorithm of type Newton is used for the problem. The solution algorithm uses a ConvergenceTest which tests convergence on the norm of the energy increment vector. Ten static load steps are performed.\nFollowing the static analysis, the wipeAnalysis and remove loadPatern commands are used to remove the nodal loads and create a new analysis. The nodal displacements have not changed. However, with the external loads removed the structure is no longer in static equilibrium.\nThe integrator for the dynamic analysis if of type GeneralizedMidpoint with α=0.5\\alpha = 0.5 . This choice is uconditionally stable and energy conserving for linear problems. Additionally, this integrator conserves linear and angular momentum for both linear and non-linear problems. The dynamic analysis is performed using 100100 time increments with a time step Δt=0.50\\Delta t = 0.50 .\nThe results consist of the file Node.out, which contains a line for every time step. Each line contains the time and the vertical displacement at the bottom center of the beam. The time history is shown in Figure 1.\n\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e"
      })
      .add(
      
      
      {
        id: 49,
        tag: "en",
        href: "/opensees-gallery/docs/advanced-settings/styles/",
        title: "Styles",
        description: "Use extensible Sass files to generate the stylesheets for your website.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 50,
        tag: "en",
        href: "/opensees-gallery/examples/shelltwist/",
        title: "Twisted Cantilever",
        description: "",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 51,
        tag: "en",
        href: "/opensees-gallery/examples/wrench/",
        title: "Wrench",
        description: "Static analysis of a wrench",
        
        
        content: "This problem is adapted from Logan (2012), Problem 7–28.\nScript: model.py\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 # ===----------------------------------------------------------------------===// # # OpenSees - Open System for Earthquake Engineering Simulation # Structural Artificial Intelligence Laboratory # stairlab.berkeley.edu # # ===----------------------------------------------------------------------===// # # Static analysis of a wrench in the plane. # # The mesh is created from 7 blocks: # ______ # / / # / / # / / # / / # / / # / / # / / # / / # / 7 / # /_____/ ____ # / \\ # / 6 \\ 70 # /_____________\\ ____ # | \\ / | # | \\ 3 / | 20 # | 4 \\_______/ 2 | _________ # |___/ \\___| ____ 20 # \\5 | | 1/ 70 # \\_| |_/ __ # . o ____ __ 10 # ^ # # # # Chrystal Chern and Claudio Perez # import sees import opensees.openseespy as ops import numpy as np angwrench = np.arctan(1/5) # Quadrilateral blocks that comprise the wrench: blocks =  1:  1: [ 0, 0], 2: [ 20, 10], 3: [ 40, 160-70-40], 4: [ 0, 160-70-40], 6: [ 35, 30], # 6: [ 25, 30], 2:  1: [ 0, 160-70-40], 2: [ 40, 160-70-40], # 6: [ 45, 160-70-20], 3: [ 40, 160-70 ], 4: [ -20, 160-70-20], 3:  1: [ -20, 160-70-20], 2: [ 40, 160-70 ], 3: [-115, 160-70 ], 4: [ -60, 70], 4:  1: [ -60, 70], 2: [-115, 90], 3: [-115, 50], 4: [ -75, 50], 5:  1: [ -75, 50], 2: [-115, 50], 3: [ -95, 10], 4: [ -75, 0], 6:  1: [ 40, 90], 5: [ 33, 112], 2: [ 0, 160], 3: [-50*np.cos(angwrench), 160 + 50*np.sin(angwrench)], 4: [-115, 160-70 ], 7:  1: [ 0, 160], 2: [250*np.sin(angwrench), 160+250*np.cos(angwrench)], 3: [250*np.sin(angwrench)-50*np.cos(angwrench), 160+250*np.cos(angwrench)], 4: [-50*np.cos(angwrench), 160+ 50*np.sin(angwrench)]  # Subdivisions to create within each block: divs =  1: (3,3), 2: (3,3), 3: (3,4), 4: (3,3), 5: (3,3), 6: (4,4), 7: (6,4)  def create_quads(): model = ops.Model(ndm=2, ndf=2) model.nDMaterial(\u0026#34;ElasticIsotropic\u0026#34;, 1, 200e3, 0.25) for num,block in blocks.items(): model.surface(divs[num], element=\u0026#34;quad\u0026#34;, args=(1, \u0026#34;PlaneStrain\u0026#34;, 1), points = block) return model def create_tris(): model = ops.Model(ndm=2, ndf=2) model.nDMaterial(\u0026#34;ElasticIsotropic\u0026#34;, 1, 200e3, 0.25) elem = 1 for num,block in blocks.items(): # Because no element argument is passed, only nodes are created. # Next we will go back over the newly created cells and manually # create triangles. mesh = model.surface(divs[num], points = block) # For each new 4-node cell, create two triangles for cell in mesh.cells: nodes = mesh.cells[cell] model.element(\u0026#34;tri31\u0026#34;, elem, (nodes[0], nodes[1], nodes[2]), 10, \u0026#34;PlaneStrain\u0026#34;, 1) model.element(\u0026#34;tri31\u0026#34;, elem+1, (nodes[0], nodes[2], nodes[3]), 10, \u0026#34;PlaneStrain\u0026#34;, 1) elem += 2 return model def create_boundary(model): # Load magnitude P = 700 # Fix the first node, which is at (0.0, 0.0) model.fix(1, 1, 1) # Create a load pattern model.pattern(\u0026#34;Plain\u0026#34;, 1, \u0026#34;Linear\u0026#34;) for node in model.getNodeTags(): coord = model.nodeCoord(node) # Fix corner of block 4 if np.linalg.norm(np.array(coord) - blocks[4][4]) \u0026lt; 1e-12: model.fix(node, 1,1) # Add load to the corner of block 7 elif np.linalg.norm(np.array(coord) - blocks[7][3]) \u0026lt; 1e-12: model.load(node, (P, 0), pattern=1) #model = create_quads() model = create_tris() create_boundary(model) model.analysis(\u0026#34;Static\u0026#34;) model.integrator(\u0026#34;LoadControl\u0026#34;, 1) model.analyze(1) # Render the deformed shape sees.serve(sees.render(model, lambda i: [500*u for u in model.nodeDisp(i)], canvas=\u0026#34;gltf\u0026#34;)) References \u0026nbsp; Logan, D.L. (2012) A First Course in the Finite Element Method. 5th ed. Stamford, CT: Cengage Learning."
      })
      ;
  

  search.addEventListener('input', showResults, true);
}
  
function hideSuggestions(e) {
  var isClickInsideElement = suggestions.contains(e.target);

  if (!isClickInsideElement) {
    suggestions.classList.add('d-none')
    if (background !== null ) {
      background.style.setProperty('--image-opacity', '0.1')
    }
  }
}

/*
Source:
  - https://raw.githubusercontent.com/h-enk/doks/master/assets/js/index.js
*/
function inputFocus(e) {
  if (e.ctrlKey && e.key === '/' ) {
    e.preventDefault();
    search.focus();
  }
  if (e.key === 'Escape' ) {
    search.blur();
    suggestions.classList.add('d-none');
  }
}

/*
Source:
  - https://dev.to/shubhamprakash/trap-focus-using-javascript-6a3
*/
function suggestionFocus(e) {
  const suggestionsHidden = suggestions.classList.contains('d-none');
  if (suggestionsHidden) return;

  const focusableSuggestions= [...suggestions.querySelectorAll('a')];
  if (focusableSuggestions.length === 0) return;

  const index = focusableSuggestions.indexOf(document.activeElement);

  if (e.key === "ArrowUp") {
    e.preventDefault();
    const nextIndex = index > 0 ? index - 1 : 0;
    focusableSuggestions[nextIndex].focus();
  }
  else if (e.key === "ArrowDown") {
    e.preventDefault();
    const nextIndex= index + 1 < focusableSuggestions.length ? index + 1 : index;
    focusableSuggestions[nextIndex].focus();
  }
}
  
/*
Source:
  - https://github.com/nextapps-de/flexsearch#index-documents-field-search
  - https://raw.githack.com/nextapps-de/flexsearch/master/demo/autocomplete.html
*/
function showResults() {
  const maxResult = 5;
  var searchQuery = this.value;
  // filter the results for the currently tagged language
  const lang = document.documentElement.lang;
  var results = null;
  if (searchQuery) {
    results = index.search(searchQuery, { index: ['title', 'description', 'content'], limit: maxResult, tag: lang, enrich: true });
    if (background !== null) {
      background.style.setProperty('--image-opacity', '0')
    }
  } else {
    if (background !== null) {
      background.style.setProperty('--image-opacity', '0.1')
    }
  }

  // flatten results since index.search() returns results for each indexed field
  const flatResults = new Map(); // keyed by href to dedupe results
  if (results !== null) {
    for (const result of results.flatMap(r => r.result)) {
      if (flatResults.has(result.doc.href)) continue;
      flatResults.set(result.doc.href, result.doc);
    }
  }

  suggestions.innerHTML = "";
  suggestions.classList.remove('d-none');
  
  // inform user that no results were found
  if (flatResults.size === 0 && searchQuery) {
    const msg = suggestions.dataset.noResults;
    const noResultsMessage = document.createElement('div')
    noResultsMessage.innerHTML = `${msg} "<strong>${searchQuery}</strong>"`
    noResultsMessage.classList.add("suggestion__no-results");
    suggestions.appendChild(noResultsMessage);
    return;
  }

  // construct a list of suggestions
  for (const [href, doc] of flatResults) {
    const entry = document.createElement('div');
    suggestions.appendChild(entry);

    const a = document.createElement('a');
    a.href = href;
    entry.appendChild(a);

    const title = document.createElement('span');
    title.classList.add('text-start');
    title.textContent = doc.title;
    title.classList.add("suggestion__title");
    a.appendChild(title);

    const description = document.createElement('span');
    description.textContent = doc.description;
    description.classList.add("suggestion__description");
    a.appendChild(description);

    suggestions.appendChild(entry);

    if (suggestions.childElementCount == maxResult) break;
  }
}
  
if (search !== null && suggestions !== null) {
  document.addEventListener('keydown', inputFocus);
  document.addEventListener('keydown', suggestionFocus);  
  document.addEventListener('click', hideSuggestions);
  initIndex();
}

const searchModal = document.getElementById('search-modal')
if (searchModal !== null) {
  searchModal.addEventListener('shown.bs.modal', function () {
    const searchInput = document.getElementById('search-input-modal')
    if (searchInput !== null) {
      searchInput.focus({ focusVisible: true })
    }
  })
}

;
document.querySelectorAll('.dynamic-svg').forEach((placeholder) => {
  placeholder.onload = function () {
    const container = placeholder.parentElement
    const doc = placeholder.contentDocument
    const attr = placeholder.getAttribute('data-class')
    const style = placeholder.getAttribute('data-style')

    if (container !== null && doc !== null) {
      const svg = doc.querySelector('svg')
      if (svg !== null) {
        svg.setAttribute('class', 'svg-inline--fa ' + (attr || ''))
        svg.setAttribute('fill', 'currentcolor')
        svg.setAttribute('aria-hidden', 'true')
        svg.setAttribute('role', 'img')
        if (style !== null && style !== '') {
          svg.setAttribute('style', style)
        }
        svg.removeAttribute('height')
        svg.removeAttribute('width')
        container.innerHTML = ''
        container.appendChild(svg)
      }
    }
  }
})

;
const fixed = true
const navbar = document.querySelector('.navbar')
const togglers = document.querySelectorAll('.main-nav-toggler')
const modeSelectors = document.querySelectorAll('.switch-mode-collapsed')
const colorsBG = ['body', 'secondary', 'tertiary']

function updateNavbar () {
  if (window.scrollY > 75) {
    navbar.classList.add('nav-active')
    const storedTheme = localStorage.getItem('theme')
    navbar.setAttribute('data-bs-theme', storedTheme)
  } else {
    navbar.classList.remove('nav-active')
    const defaultTheme = navbar.getAttribute('data-bs-overlay')

    if (defaultTheme) {
      navbar.setAttribute('data-bs-theme', defaultTheme)
    }
  }
}

if ((navbar !== null) && (window.performance.getEntriesByType)) {
  if (window.performance.getEntriesByType('navigation')[0].type === 'reload') {
    fixed && updateNavbar()
  }
}

if (navbar !== null && togglers !== null) {
  // observe state changes to the site's color mode
  const html = document.querySelector('html')
  const config = {
    attributes: true,
    attributeFilter: ['data-bs-theme']
  }
  const Observer = new MutationObserver((mutationrecords) => {
    fixed && updateNavbar()
  })
  Observer.observe(html, config)

  // initialize background color
  const color = (navbar.getAttribute('data-navbar-color') || 'body')
  const bg = colorsBG.includes(color) ? `var(--bs-${color}-bg)` : `var(--bs-navbar-color-${color})`
  navbar.style.setProperty('--bs-navbar-expanded-color', bg)

  // set the navbar background color to opaque when scrolling past a breakpoint
  window.onscroll = () => {
    fixed && updateNavbar()
  }

  // set the navbar background color to opaque when expanded
  for (let i = 0; i < togglers.length; ++i) {
    togglers[i].onclick = () => {
      navbar.classList.toggle('navbar-expanded')
    }
  }

  // invoke the navbar toggler for each mode switcher to collapse the main menu afterwards
  for (let i = 0; i < modeSelectors.length; ++i) {
    modeSelectors[i].onclick = () => {
      for (let j = 0; j < togglers.length; ++j) {
        const toggler = togglers[j]
        if (toggler.getAttribute('aria-expanded') === 'true') {
          toggler.click()
        }
      }
    }
  }
}

;
const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
// eslint-disable-next-line no-undef, no-unused-vars
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

;;
// Script to move all embedded toast messages into a container with id 'toast-container'. The container ensures multiple
// toast messages are stacked properly. The script targets all elements specified by a 'data-toast-target' and ensures
// the click event of the origin is linked as well.

const container = document.getElementById('toast-container')
if (container !== null) {
  // process all data-toast-target elements
  document.querySelectorAll('[data-toast-target]').forEach(trigger => {
    const target = document.getElementById(trigger.getAttribute('data-toast-target'))
    if (target !== null) {
      // move the element to the toast containr
      container.appendChild(target)

      // eslint-disable-next-line no-undef
      const toast = bootstrap.Toast.getOrCreateInstance(target)
      if (toast !== null) {
        // associate the click event of the origin with the toast element
        trigger.addEventListener('click', () => {
          toast.show()
        })
      }
    }
  })
}

;
// Bootstrap tooltip example: https://getbootstrap.com/docs/5.2/components/tooltips/
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
// eslint-disable-next-line no-unused-vars, no-undef
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

;
document.querySelectorAll('[data-video-padding]').forEach(element => {
  element.style.paddingBottom = element.getAttribute('data-video-padding')
})
