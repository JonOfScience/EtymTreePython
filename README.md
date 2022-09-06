<style>.mermaid svg { height: auto; }</style>

# EtymTreePython
A python designed to allow input, display, and tracking of the vocabulary of a constructed language.

## Configuration
```mermaid
sequenceDiagram
    actor Config
    Participant ConfigManager
    participant ConfigService
    participant IOService
    participant Deserialiser
    participant TypeDeserialiser
    
    rect rgb(200, 200, 200)
    Config->>ConfigManager: import_config() CM_IC_0
    end

    rect rgb(200, 200, 200)
    ConfigManager->>ConfigService: import_config() CM_IC_1
    end

    rect rgb(200, 255, 150)
    ConfigService->>IOService: deserialise_stored() CM_IC_2
    end

    activate IOService
    
    rect rgb(200, 255, 150)
    IOService->>IOService: read() data from file CM_IC_3
    end
    
    rect rgb(200, 255, 150)
    IOService->>IOService: deserialise_string_to_obj(data) CM_IC_4
    end
    
    rect rgb(200, 255, 150)
    IOService->>Deserialiser: deserialise(data) CM_IC_5
    end
    
    deactivate IOService
    
    rect rgb(200, 255, 150)
    Deserialiser->>TypeDeserialiser: deserialise(data) CMI_IC_6
    end

    rect rgb(200, 255, 150)
    activate TypeDeserialiser
    Note over TypeDeserialiser: data to dict
    TypeDeserialiser->>Deserialiser: return dict CM_IC_7
    end
    deactivate TypeDeserialiser

    rect rgb(200, 255, 150)
    Deserialiser->>IOService: return dict CM_IC_8
    end

    rect rgb(200, 255, 150)
    IOService->>ConfigService: return dict CM_IC_9
    end

    rect rgb(200, 200, 200)
    ConfigService->>ConfigManager: return dict CM_IC_10
    end

    rect rgb(200, 200, 200)
    activate ConfigManager
    ConfigManager->>ConfigManager: integrate_config_dict() CM_IC_11
    end
    deactivate ConfigManager
    
    rect rgb(200, 200, 200)
    ConfigManager ->> Config: UPDATED CM_IC_12
    end
```

| Test Code | Information |
|-|-|
| CM_IC_0 | 
| |
| CM_IC_1 |
| |
| **CM_IC_2** | GivenANewConfigService:
| | CM_IC_2_AServiceWillCallDeserialiseStoredOnImport
| |
| **CM_IC_3** | GivenANewIOService
| | CM_IC_3_TheServiceCallsReadOnDeserialise
| |
| **CM_IC_4** | GivenANewIOService
| | CM_IC_4_TheServiceCallsDeserialiseStringToObjectOnDeserialise 
| |
| **CM_IC_5** | GivenAnIOServiceInJSONFormat
| | CM_IC_5_TheServiceWillCallDeserializeString
| |
| **CM_IC_6** | GivenADeserialiserInJSONFormat
| | CM_IC_6_AJSONDeserialiserIsCalled
| |
| **CM_IC_7** | GivenADeserialiserInJSONFormat 
| | CM_IC_7_AJSONStringCanBeDeserialised |
| |
| **CM_IC_8** | GivenADeserialiserInJSONFormat 
| | test_CM_IC_8_TheServiceWillDeserialiseAStoredString
| |
| **CM_IC_9** | GivenANewConfigService:
| | CM_IC_9_AServiceReturnADeserialisedObjectOnImport
| |
| CM_IC_10 |
| |
| CM_IC_11 |
| |
| CM_IC_12 |
