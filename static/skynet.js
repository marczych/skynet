'use strict';

const {
  Button,
  CircularProgress,
  Container,
  Grid,
  Icon,
  Typography,
} = MaterialUI;

const COMMAND_PREFIXES = [
  "ONE",
  "TWO",
  "THREE",
];

const COMMANDS = [
  { name: "Open", command: "UP" },
  { name: "Stop", command: "STOP" },
  { name: "Close", command: "DOWN" },
];

const STATUS_PENDING = "pending";
const STATUS_SUCCESS = "success";
const STATUS_ERROR = "error";

function App() {
  // Status of any requests.
  const [status, setStatus] = React.useState(undefined);

  return (
    <Container maxWidth="sm">
      <div style={{ marginTop: 24 }}>
        <Grid
          container
          direction="row"
          justify="flex-start"
          alignItems="center"
        >
          <Typography variant="h4" component="h1" gutterBottom>
            Skynet
          </Typography>

          <div style={{ marginLeft: 8 }}>
            { status === STATUS_PENDING && <CircularProgress /> }
            { status === STATUS_SUCCESS &&
              <Icon style={{ color: "#4caf50" }}>check_circle</Icon>
            }
            { status === STATUS_ERROR &&
              <Icon style={{ color: "#f44336" }}>error</Icon>
            }
          </div>
        </Grid>

        <Grid container spacing={ 1 }>
          {COMMAND_PREFIXES.map((command) => (
            <CommandRow
              key={ command }
              commandPrefix={ command }
              setStatus={ setStatus }
            />
          ))}
        </Grid>
      </div>
    </Container>
  );
}

function CommandRow({commandPrefix, setStatus}) {
  return (
    <React.Fragment>
      <Grid container item xs={ 12 } spacing={ 3 } alignItems="center">
        <Grid container item xs={ 3 }>
          <Typography>{ commandPrefix }</Typography>
        </Grid>

        {COMMANDS.map(({ name, command }) => (
          <Grid key={ command } container item xs={ 3 }>
            <CommandButton
              name={ name }
              command={ `${commandPrefix}_${command}` }
              setStatus={ setStatus }
            />
          </Grid>
        ))}
      </Grid>
    </React.Fragment>
  );
}

function CommandButton({ name, command, setStatus }) {
  function sendCommand() {
    setStatus(STATUS_PENDING);

    fetch(
      "/api/command",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ command: command }),
      },
    ).then((response) => {
      if (response.status === 200) {
        setStatus(STATUS_SUCCESS);
      } else {
        setStatus(STATUS_ERROR);
        console.error(response);
      }
    }).catch((error) => {
      setStatus(STATUS_ERROR);
      console.error(error);
    });
  }

  return (
    <Button onClick={ sendCommand } variant="contained">{ name }</Button>
  );
}

ReactDOM.render(React.createElement(App), document.querySelector("#app"));
