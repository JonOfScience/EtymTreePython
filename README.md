<style>.mermaid svg { height: auto; }</style>

# EtymTreePython
A python project designed to allow input, display, and tracking of the vocabulary of a constructed language.

## Configuration (V1)
```mermaid
sequenceDiagram
    actor Config
    Participant Settings
    participant ConfigService
    participant IOService
    participant Deserialiser
    participant TypeDeserialiser
    
    rect rgb(200, 200, 200)
    Config->>Settings: import_config() CM_IC_0
    end

    rect rgb(200, 255, 150)
    Settings->>ConfigService: import_config() CM_IC_1
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
    ConfigService->>Settings: return dict CM_IC_10
    end

    rect rgb(200, 255, 150)
    activate Settings
    Settings->>Settings: integrate_config() CM_IC_11
    end
    deactivate Settings
    
    rect rgb(200, 255, 150)
    Settings ->> Config: UPDATED CM_IC_12
    end
```

| Test Code | Information |
|-|-|
| CM_IC_0 | 
| |
| **CM_IC_1** | GivenEmptySettings
| | cm_ic_1_a_request_to_import_configuration_options_is_passed_on
| |
| **CM_IC_2** | GivenANewConfigService
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
| **CM_IC_10** | GivenANewConfigManager
| | CM_IC_10_ImportConfigReturnsAConfigDictionary
| |
| **CM_IC_11** | GivenEmptySettings
| | test_when_a_valid_id_is_specified_then_the_expected_setting_value_is_returned
| |
| **CM_IC_12** | GivenAnExistingConfiguration
| | cm_ic_12_base_entries_are_overwritten_when_importing_config


## IOService Tests: IOS (./tests/test_io_service.py)

### IOService Read Tests: IOS-RDF
```mermaid
sequenceDiagram
    actor Test
    participant IOService
    Test->>IOService: read(filename: str)
    rect rgb(200, 200, 200)
    IOService->>Test: file_data
    end
```

| Label | Path | Description | Include? | Complete
|-|-|-|-|-|
| IOS-RDF-00 | Happy | Reads data from file in UTF-8 | :heavy_check_mark: | No
| IOS-RDF-01 | Sad | File doesn't exist | :heavy_check_mark: | No
| IOS-RDF-02 | Bad | Incorrect file format | :x:


## Configuration
```mermaid
sequenceDiagram
    actor Config
    Participant Settings
    participant ConfigService
    participant IOService
    participant Deserialiser
    participant TypeDeserialiser
    
    rect rgb(200, 200, 200)
    Config->>Settings: import_config()
    end

    rect rgb(200, 255, 150)
    Settings->>ConfigService: import_config()
    end

    rect rgb(200, 255, 150)
    ConfigService->>IOService: des  erialise_stored()
    end

    activate IOService
    
    rect rgb(200, 255, 150)
    IOService->>IOService: read() data from file
    end
    
    rect rgb(200, 255, 150)
    IOService->>IOService: deserialise_string_to_obj(data)
    end
    
    rect rgb(200, 255, 150)
    IOService->>Deserialiser: deserialise(data)
    end
    
    deactivate IOService
    
    rect rgb(200, 255, 150)
    Deserialiser->>TypeDeserialiser: deserialise(data)
    end

    rect rgb(200, 255, 150)
    activate TypeDeserialiser
    Note over TypeDeserialiser: data to dict
    TypeDeserialiser->>Deserialiser: return dict
    end
    deactivate TypeDeserialiser

    rect rgb(200, 255, 150)
    Deserialiser->>IOService: return dict
    end

    rect rgb(200, 255, 150)
    IOService->>ConfigService: return dict
    end

    rect rgb(200, 200, 200)
    ConfigService->>Settings: return dict
    end

    rect rgb(200, 255, 150)
    activate Settings
    Settings->>Settings: integrate_config()
    end
    deactivate Settings
    
    rect rgb(200, 255, 150)
    Settings ->> Config: UPDATED
    end
```
