ARG ROS_DISTRO=humble
ARG SIMULATION=TRUE



FROM ros:${ROS_DISTRO}-ros-core-jammy
ENV ROS_DISTRO=${ROS_DISTRO}
ENV SIMULATION=TRUE




############################################################
############################################################
ENV DISPLAY=host.docker.internal:0.0
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install --yes pulseaudio-utils
# Example of installing programs
RUN apt-get update \
    && apt-get install -y \
    nano \
    vim \
    && rm -rf /var/lib/apt/lists/*
# Set the timezone non-interactively
ARG TZ=Asia/Kolkata
ENV DEBIAN_FRONTEND=noninteractive
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# Create a non-root user
ARG USERNAME=ros
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
  && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
  && mkdir /home/$USERNAME/.config && chown $USER_UID:$USER_GID /home/$USERNAME/.config         
RUN usermod -aG dialout ${USERNAME}
# Set up sudo
RUN apt-get update \
  && apt-get install -y sudo \
  && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
  && chmod 0440 /etc/sudoers.d/$USERNAME\
  && rm -rf /var/lib/apt/lists/*
# Switch from root to user
USER $USERNAME
# Add user to video group to allow access to webcam
RUN sudo usermod --append --groups video $USERNAME
USER root
RUN chmod 1777 /var/tmp
RUN chmod -R 777 /var/tmp/
# COPY pulse-client.conf /etc/pulse/client.conf
############################################################
############################################################










####################
# gazebo install
# Install required tools
# Install required utilities
RUN if [ "${SIMULATION}" = "TRUE" ]; then \
        apt-get update && apt-get install -y \
        wget \
        curl \
        gnupg \
        lsb-release \
        && apt-get clean; \
        else \
        echo "Skipping Gazebo installation as SIMULATION is set to FALSE"; \
        fi
RUN if [ "${SIMULATION}" = "TRUE" ]; then \
        apt-get install -y ros-humble-desktop-full; \
        else \
        echo "Skipping Gazebo installation as SIMULATION is set to FALSE"; \
        fi
RUN if [ "${SIMULATION}" = "TRUE" ]; then \
    echo "deb http://packages.osrfoundation.org/gazebo/ubuntu `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list \
    && wget http://packages.osrfoundation.org/gazebo.key -O - | apt-key add - \
    && apt-get update \
    && apt-get install -y \
    gazebo \
    ros-${ROS_DISTRO}-gazebo-ros-pkgs \
    && apt-get clean; \
    else \
    echo "Skipping Gazebo installation as SIMULATION is set to FALSE"; \
    fi
# # gazebo packages
# RUN if [ "${SIMULATION}" = "TRUE" ]; then \
#         curl -L https://github.com/osrf/gazebo_models/archive/refs/heads/master.zip -o /tmp/gazebo_models.zip \
#         && unzip /tmp/gazebo_models.zip -d /tmp && mkdir -p ~/.gazebo/models/ && mv /tmp/gazebo_models-master/* ~/.gazebo/models/ \
#         && rm -r /tmp/gazebo_models.zip; \
#     fi
####################




















############################################################
############################################################
# basic installation
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y git
RUN git config --global --add safe.directory /robot
RUN apt-get install -y python3-pip
WORKDIR /robot
############################################################
############################################################






# cd ~/Downloadsrobot
RUN git clone https://github.com/wbeebe/WiringPi.git
WORKDIR /robot/WiringPi/
RUN ./build
WORKDIR /robot






############################################################
############################################################
# Add ROS repository and key
RUN apt-get update && apt-get install -y \
    gnupg2 \
    lsb-release
RUN sh -c 'echo "deb http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list'
RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
# Update package lists
RUN apt-get update
ARG ROS_DISTRO=humble
############################################################
############################################################









############################################################
############################################################
# ros packages
RUN apt-get install -y ros-dev-tools
RUN apt-get install -y ros-${ROS_DISTRO}-ament-cmake
RUN apt-get install -y ros-${ROS_DISTRO}-ament-cmake-clang-format
RUN apt-get install -y ros-${ROS_DISTRO}-ament-lint-auto
RUN apt-get install -y ros-${ROS_DISTRO}-twist-mux
# Use Cyclone DDS as middleware
RUN apt-get update && apt-get install -y --no-install-recommends \
 ros-${ROS_DISTRO}-rmw-cyclonedds-cpp
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
# RUN dpkg --configure -a
# RUN apt-get -y install --fix-broken
# RUN apt-get -y update
# RUN apt-get -y upgrade
## control
RUN apt-get install -y ros-${ROS_DISTRO}-xacro
RUN apt-get install -y ros-${ROS_DISTRO}-joint-state-publisher
RUN apt-get install -y ros-${ROS_DISTRO}-robot-state-publisher
RUN apt-get install -y ros-${ROS_DISTRO}-ros2-control
RUN apt-get install -y ros-${ROS_DISTRO}-ros2-controllers
RUN apt-get install -y ros-${ROS_DISTRO}-tf-transformations
# localization
RUN apt-get install -y ros-${ROS_DISTRO}-imu-tools
RUN apt-get install -y libi2c-dev i2c-tools libi2c0
RUN apt-get install -y ros-${ROS_DISTRO}-robot-localization 
RUN apt-get install -y i2c-tools
RUN apt-get install -y ros-${ROS_DISTRO}-rosbridge-suite
############################################################
############################################################































############################################################
############################################################
## sound
RUN apt-get install -y alsa-utils pulseaudio socat ffmpeg
ENV PULSE_SERVER=host.docker.internal
RUN apt-get install -y festival festival-dev
RUN apt-get install -y festival festlex-cmu festlex-poslex festlex-oald unzip
RUN apt-get install -y python3-pyaudio
RUN apt-get install -y pavucontrol
RUN apt-get install -y libportaudio2
RUN apt-get install -y libasound-dev
RUN apt-get install -y alsa-oss
RUN apt-get install -y oss-compat
RUN apt-get install -y flac
RUN apt-get install -y sox
RUN apt-get install -y libttspico-utils
# RUN apt-get install -y osspd
# RUN apt-get install -y osspd-alsa
# RUN modprobe snd-pcm-oss
# RUN apt-get install -y gedit
## for display ui
## pavucontrol ## run to check audio input and output
# Install package dependencies
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        alsa-base \
        alsa-utils \
        libsndfile1-dev && \
    apt-get clean
############################################################
############################################################























################################################################################
################################################################################
######################### ahilya ###############################################
## navigation
RUN apt-get install -y ros-${ROS_DISTRO}-navigation2
RUN apt-get install -y ros-${ROS_DISTRO}-nav2-bringup
RUN apt-get install -y ros-${ROS_DISTRO}-slam-toolbox
RUN apt-get install -y ros-${ROS_DISTRO}-cartographer-ros
RUN apt-get install -y ros-${ROS_DISTRO}-nav2-velocity-smoother
## hardware
RUN apt-get install -y ros-${ROS_DISTRO}-rplidar-ros
## fix broken and update
RUN dpkg --configure -a
RUN apt-get -y install --fix-broken
RUN apt-get -y update
RUN apt-get -y upgrade
################################################################################
################################################################################
































############################################################
############################################################
WORKDIR /robot/src
###############  xparo_ros  ###############
RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxslt-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
RUN git clone https://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@github.com/lazyxcientist/xparo_ros.git
RUN pip install --no-cache-dir -r /robot/src/xparo_ros/requirements.txt 
###############  xparo_dashboard ###############
RUN git clone https://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@github.com/lazyxcientist/xparo_dashboard.git
RUN pip install --no-cache-dir -r /robot/src/xparo_dashboard/requirements.txt 
###############  xparo_listen  ###############
RUN apt-get install -y \
    # libasound2 \
    libasound2-dev
RUN git clone https://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@github.com/lazyxcientist/xparo_listen.git
RUN pip install --no-cache-dir -r /robot/src/xparo_listen/requirements.txt
WORKDIR /var/tmp/xparo/listen/
RUN wget https://alphacephei.com/vosk/models/vosk-model-small-en-in-0.4.zip
RUN unzip vosk-model-small-en-in-0.4.zip
RUN rm vosk-model-small-en-in-0.4.zip
###############  xparo_speak  ###############
WORKDIR /var/tmp/xparo/speak/
# Ensure the directory exists and create a dummy .wav file
RUN mkdir -p /var/tmp/xparo/speak && \
    sox -n -r 44100 -c 2 /var/tmp/xparo/speak/tts.wav synth 1 sine 440 && \
    sox /var/tmp/xparo/speak/tts.wav /var/tmp/xparo/speak/tts_adjusted.wav
RUN chmod -R 777 /var/tmp/xparo/speak
# Or, create empty dummy files
# RUN mkdir -p /var/tmp/xparo/speak && touch /var/tmp/xparo/speak/tts.wav /var/tmp/xparo/speak/tts_adjusted.wav
WORKDIR /robot/src/
RUN git clone https://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@github.com/lazyxcientist/xparo_speak.git
RUN pip install --no-cache-dir -r /robot/src/xparo_speak/requirements.txt 
###############  xparo_task  ###############
RUN git clone https://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@github.com/lazyxcientist/xparo_task.git
RUN pip install --no-cache-dir -r /robot/src/xparo_task/requirements.txt 
###############  xparo_settings  ###############
RUN apt-get update && apt-get install -y \
    network-manager \
    upower \
    power-profiles-daemon \
    libcups2 \
    dbus
RUN git clone https://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@github.com/lazyxcientist/xparo_settings.git
RUN pip install --no-cache-dir -r /robot/src/xparo_settings/requirements.txt 
############################################################
############################################################





















############################################################
############################################################
############### rosdep, colcon build #######################
############################################################
############################################################
# RUN apt-get update
# RUN apt-get upgrade
WORKDIR /robot
# COPY ./src /robot/src
COPY requirements.txt /robot/requirements.txt
RUN pip install --no-cache-dir -r /robot/requirements.txt
# Install Python3 and ROS-related dependencies
RUN apt-get install -y python3-serial
RUN apt-get install -y libserial-dev
RUN apt-get install -y \
    python3-colcon-common-extensions \
    python3-pip \
    python3-rosdep \
    --no-install-recommends \
    && apt-get clean
RUN rosdep init && rosdep update
# RUN /bin/bash -c 'cd /robot/ \
#     && source /opt/ros/${ROS_DISTRO}/setup.bash \
#     && rosdep install --from-paths src --ignore-src -r -y \
#     && colcon build'
# Source the ROS setup file
USER root
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc
RUN echo "source /robot/install/setup.bash" >> ~/.bashrc
RUN echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc
USER $USERNAME
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc
RUN echo "source /robot/install/setup.bash" >> ~/.bashrc
RUN echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc

# CMD ["/bin/bash", "-c", "source /opt/ros/${ROS_DISTRO}/setup.bash && source /robot/install/setup.bash && ros2 launch core final_robot.launch.py"]
############################################################
############################################################






