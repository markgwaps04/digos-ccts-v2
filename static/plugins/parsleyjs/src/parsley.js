import $ from 'jquery';
import Parsley from 'parsleyjs/src/parsley/main';
import 'parsleyjs/src/parsley/pubsub';
import './parsley/remote';
import './i18n/en';
import inputevent from './vendor/inputevent';

inputevent.install();

export default Parsley;
