from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from dataclass_csv import accept_whitespaces, dateformat


@dataclass
class Preheader:
    format_version: str
    app_release: Optional[str] = None
    model: Optional[str] = None
    release: Optional[str] = None
    device: Optional[str] = None
    display: Optional[str] = None
    board: Optional[str] = None
    brand: Optional[str] = None


fields = {
    "MAC": "address",
    "SSID": "name",
    "AuthMode": "capabilities",
    "FirstSeen": "timestamp",
    "Channel": "channel",
    "RSSI": "rssi",
    "CurrentLatitude": "latitude",
    "CurrentLongitude": "longitude",
    "AltitudeMeters": "altitude",
    "AccuracyMeters": "accuracy",
    "Type": "type",
}


@accept_whitespaces
@dataclass
@dateformat("%Y-%m-%d %H:%M:%S")
class Radio:  # WiFi, Cell, Bluetooth
    address: str  # bssid, cell key, address
    capabilities: str
    timestamp: datetime
    channel: int  # channel, frequency, channel
    rssi: int
    latitude: float
    longitude: float
    altitude: float
    accuracy: float
    type: str
    # some don't broadcast a name
    name: Optional[str] = None  # ssid, name, name
